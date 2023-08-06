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
    name: str|None = None
    output_names: tuple[str]|None = None
    label_names: tuple[str]|None = None

    def __post_init__(self):
        if self.name is None:
            self.name = self.__class__.__name__
        self.reset()

    def reset(self):
        """将内部评估结果重置为初始状态。"""
        self.num_inst = 0
        self.sum_metric = 0.0

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
    
    # def update_dict(self, label, pred):
    #     """Update the internal evaluation with named label and pred

    #     Parameters
    #     ----------
    #     labels : OrderedDict of str -> NDArray
    #         name to array mapping for labels.

    #     preds : OrderedDict of str -> NDArray
    #         name to array mapping of predicted outputs.
    #     """
    #     if self.output_names is not None:
    #         pred = [pred[name] for name in self.output_names]
    #     else:
    #         pred = list(pred.values())

    #     if self.label_names is not None:
    #         label = [label[name] for name in self.label_names]
    #     else:
    #         label = list(label.values())

    #     self.update(label, pred)
    
    @abstractmethod
    def update(self, labels: np.ndarray, preds: np.ndarray):
        """更新内部评估结果。

        Args:
            labels: data 的标签。
            preds: data 的预测值。
        """
        ...

@dataclass
class Accuracy(EvalMetric):
    """计算 accuracy classification 得分。

    accuracy 定义如下::

    .. math::
        \\text{accuracy}(y, \\hat{y}) = \\frac{1}{n} \\sum_{i=0}^{n-1}
        \\text{1}(\\hat{y_i} == y_i)
            
    Examples:
        >>> predicts = np.array([[0.3, 0.7], [0, 1.], [0.4, 0.6]])
        >>> labels   = np.array([0, 1, 1])
        >>> acc = Accuracy("acc")
        >>> acc.update(preds = predicts, labels = labels)
        >>> acc.get()
        ('accuracy', 0.6666666666666666)
        >>> predicts = np.array([1, 0])
        >>> labels   = np.array([0, 1])
        >>> metric.update(preds = predicts, labels = labels)
        >>> metric.get()
        ('accuracy', 0.4)
    """
    def update(self, labels: np.ndarray, preds: np.ndarray):
        """更新内部评估结果。

        Args:
            labels: 数据的标签，以类别索引作为值，每个样本一个标签。
            preds: 样本的预测值。每个预测值可以是类别索引，也可以是所有类别可能性的向量。
        """
        assert labels.ndim==1, "真实标签维度为 1"
        if preds.ndim==2:
            pred_labels = np.argmax(preds, axis=1)
        elif preds.ndim==1:
            pred_labels = preds
        else:
            raise f"暂时未支持预测标签维度为 {preds.ndim}"
        pred_labels = pred_labels.astype('int32')
        labels = labels.astype('int32')
        # print(pred_label.shape, label.shape)
        # 在检查形状之前进行扁平化，以避免形状不匹配。
        labels = labels.flat
        pred_labels = pred_labels.flat
        # check_label_shapes(label, pred_label)
        num_correct = (pred_labels == labels).sum()
        self.sum_metric += num_correct
        self.num_inst += len(pred_labels)