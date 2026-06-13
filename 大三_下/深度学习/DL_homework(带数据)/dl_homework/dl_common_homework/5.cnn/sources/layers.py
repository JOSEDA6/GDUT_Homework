from builtins import range
import numpy as np


def affine_forward(x, w, b):
    """Computes the forward pass for an affine (fully connected) layer.

    The input x has shape (N, d_1, ..., d_k) and contains a minibatch of N
    examples, where each example x[i] has shape (d_1, ..., d_k). We will
    reshape each input into a vector of dimension D = d_1 * ... * d_k, and
    then transform it to an output vector of dimension M.

    Inputs:
    - x: A numpy array containing input data, of shape (N, d_1, ..., d_k)
    - w: A numpy array of weights, of shape (D, M)
    - b: A numpy array of biases, of shape (M,)

    Returns a tuple of:
    - out: output, of shape (N, M)
    - cache: (x, w, b)
    """
    out = None
    ###########################################################################
    # TODO: Copy your solution.                                               #
    ###########################################################################
    # ​**​*​**START OF YOUR CODE*​**​**
    # 获取输入数据的批量大小和维度信息
    N = x.shape[0]
    # 将输入数据重塑为2D矩阵 (N, D)
    x_reshaped = x.reshape(N, -1)
    # 计算全连接层输出: out = x * w + b
    out = np.dot(x_reshaped, w) + b
    # ​**​*​**END OF YOUR CODE*​**​**
    cache = (x, w, b)
    return out, cache


def affine_backward(dout, cache):
    """Computes the backward pass for an affine (fully connected) layer.

    Inputs:
    - dout: Upstream derivative, of shape (N, M)
    - cache: Tuple of:
      - x: Input data, of shape (N, d_1, ... d_k)
      - w: Weights, of shape (D, M)
      - b: Biases, of shape (M,)

    Returns a tuple of:
    - dx: Gradient with respect to x, of shape (N, d1, ..., d_k)
    - dw: Gradient with respect to w, of shape (D, M)
    - db: Gradient with respect to b, of shape (M,)
    """
    x, w, b = cache
    dx, dw, db = None, None, None
    ###########################################################################
    # TODO: Copy your solution.                                               #
    ###########################################################################
    # ​**​*​**START OF YOUR CODE*​**​**
    # 获取输入数据的批量大小
    N = x.shape[0]
    # 将输入数据重塑为2D矩阵 (N, D)
    x_reshaped = x.reshape(N, -1)
    
    # 计算输入数据的梯度
    dx = np.dot(dout, w.T).reshape(x.shape)
    # 计算权重的梯度
    dw = np.dot(x_reshaped.T, dout)
    # 计算偏置的梯度
    db = np.sum(dout, axis=0)
    # ​**​*​**END OF YOUR CODE*​**​**
    return dx, dw, db


def relu_forward(x):
    """Computes the forward pass for a layer of rectified linear units (ReLUs).

    Input:
    - x: Inputs, of any shape

    Returns a tuple of:
    - out: Output, of the same shape as x
    - cache: x
    """
    out = None
    ###########################################################################
    # TODO: Copy your solution.                                               #
    ###########################################################################
    # ​**​*​**START OF YOUR CODE*​**​**
    # ReLU激活函数: out = max(0, x)
    out = np.maximum(0, x)
    # ​**​*​**END OF YOUR CODE*​**​**
    cache = x
    return out, cache


def relu_backward(dout, cache):
    """Computes the backward pass for a layer of rectified linear units (ReLUs).

    Input:
    - dout: Upstream derivatives, of any shape
    - cache: Input x, of same shape as dout

    Returns:
    - dx: Gradient with respect to x
    """
    dx, x = None, cache
    ###########################################################################
    # TODO: Copy your solution.                                               #
    ###########################################################################
    # ​**​*​**START OF YOUR CODE*​**​**
    # 创建与输入相同形状的梯度矩阵
    dx = np.zeros_like(x)
    # 仅在前向传播输入大于0的位置传递梯度
    dx[x > 0] = dout[x > 0]
    # ​**​*​**END OF YOUR CODE*​**​**
    return dx


def softmax_loss(x, y):
    """Computes the loss and gradient for softmax classification.

    Inputs:
    - x: Input data, of shape (N, C) where x[i, j] is the score for the jth
      class for the ith input.
    - y: Vector of labels, of shape (N,) where y[i] is the label for x[i] and
      0 <= y[i] < C

    Returns a tuple of:
    - loss: Scalar giving the loss
    - dx: Gradient of the loss with respect to x
    """
    loss, dx = None, None

    ###########################################################################
    # TODO: Copy your solution.                                               #
    ###########################################################################
    # ​**​*​**START OF YOUR CODE*​**​**
    # 获取样本数量
    N = x.shape[0]
    
    # 数值稳定性处理：减去最大值，防止指数运算溢出
    shifted_x = x - np.max(x, axis=1, keepdims=True)
    
    # 计算指数和softmax概率
    exp_x = np.exp(shifted_x)
    probs = exp_x / np.sum(exp_x, axis=1, keepdims=True)
    
    # 计算交叉熵损失
    correct_log_probs = -np.log(probs[np.arange(N), y])
    loss = np.sum(correct_log_probs) / N
    
    # 计算梯度
    dx = probs.copy()
    dx[np.arange(N), y] -= 1
    dx /= N
    # ​**​*​**END OF YOUR CODE*​**​**
    return loss, dx

