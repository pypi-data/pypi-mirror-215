from dataclasses import dataclass
from abc import ABC, abstractmethod
import numpy as np


@dataclass
class EvalMetric(ABC):
    """所有评估度量的基类。

    Args:
        name: 请提供要显示的度量实例的名称。
        output_names: 在使用 `update_dict` 进行更新时应该使用的预测名称。默认情况下，包括所有的预测名称。
        label_names: 在使用 `update_dict` 进行更新时应该使用的标签名称。默认情况下，包括所有的标签名称。
    """
    name: str
    output_names: tuple[str]|None = None
    label_names: tuple[str]|None = None

    def __post_init__(self):
        self.reset()

    def reset(self):
        """将内部评估结果重置为初始状态。"""
        self.num_inst = 0
        self.sum_metric = 0.0
        self.global_num_inst = 0
        self.global_sum_metric = 0.0

    def get(self):
        """获取当前的评估结果。

        Returns:
            names(list[str]): 度量的名称列表。
            values(list[float]): 度量的值列表。
        """
        if self.num_inst == 0:
            return (self.name, float('nan'))
        else:
            return (self.name, self.sum_metric / self.num_inst)

    def get_name_value(self):
        """返回 (名称, 值) 对。
        """
        name, value = self.get()
        if not isinstance(name, list):
            name = [name]
        if not isinstance(value, list):
            value = [value]
        return list(zip(name, value))
    
    def __str__(self):
        return f"{self.__class__.__name__}: {dict(self.get_name_value())}"
    
    def update_dict(self, label, pred):
        """Update the internal evaluation with named label and pred

        Parameters
        ----------
        labels : OrderedDict of str -> NDArray
            name to array mapping for labels.

        preds : OrderedDict of str -> NDArray
            name to array mapping of predicted outputs.
        """
        if self.output_names is not None:
            pred = [pred[name] for name in self.output_names]
        else:
            pred = list(pred.values())

        if self.label_names is not None:
            label = [label[name] for name in self.label_names]
        else:
            label = list(label.values())

        self.update(label, pred)
    
    @abstractmethod
    def update(self, labels: list[np.ndarray], preds: list[np.ndarray]):
        """更新内部评估结果。

        Args:
            labels: data 的标签列表。
            preds: data 的预测值列表。
        """
        ...

@dataclass
class Accuracy(EvalMetric):
    """计算 accuracy classification 得分。

    accuracy 定义如下::

    .. math::
        \\text{accuracy}(y, \\hat{y}) = \\frac{1}{n} \\sum_{i=0}^{n-1}
        \\text{1}(\\hat{y_i} == y_i)

    Args:
        axis: 代表类别的轴。
            

    Examples:
        >>> predicts = [np.array([[0.3, 0.7], [0, 1.], [0.4, 0.6]])]
        >>> labels   = [np.array([0, 1, 1])]
        >>> acc = Accuracy()
        >>> acc.update(preds = predicts, labels = labels)
        >>> acc.get()
        ('accuracy', 0.6666666666666666)
    """
    axis: int = 1

    def update(self, labels: list[np.ndarray], preds: list[np.ndarray]):
        """更新内部评估结果。

        Args:
            labels: 数据的标签列表，以类别索引作为值，每个样本一个标签。
            preds: 样本的预测值列表。每个预测值可以是类别索引，也可以是所有类别可能性的向量。
        """
        # labels, preds = check_label_shapes(labels, preds, True)
        if isinstance(labels, np.ndarray):
            labels = [labels]
        if isinstance(labels, np.ndarray):
            preds = [preds]
        for label, pred_label in zip(labels, preds):
            if pred_label.shape != label.shape:
                pred_label = np.argmax(pred_label, axis=self.axis)
            pred_label = pred_label.astype('int32')
            label = label.astype('int32')
            # print(pred_label.shape, label.shape)
            # 在检查形状之前进行扁平化，以避免形状不匹配。
            label = label.flat
            pred_label = pred_label.flat
            # check_label_shapes(label, pred_label)
            num_correct = (pred_label == label).sum()
            self.sum_metric += num_correct
            self.global_sum_metric += num_correct
            self.num_inst += len(pred_label)
            self.global_num_inst += len(pred_label)