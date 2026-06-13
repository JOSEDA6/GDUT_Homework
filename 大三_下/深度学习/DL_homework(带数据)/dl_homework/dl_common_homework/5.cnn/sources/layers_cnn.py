from builtins import range
import numpy as np
from .layers import *

def conv_forward_naive(x, w, b, conv_param):
    """A naive implementation of the forward pass for a convolutional layer.

    The input consists of N data points, each with C channels, height H and
    width W. We convolve each input with F different filters, where each filter
    spans all C channels and has height HH and width WW.

    Input:
    - x: Input data of shape (N, C, H, W)
    - w: Filter weights of shape (F, C, HH, WW)
    - b: Biases, of shape (F,)
    - conv_param: A dictionary with the following keys:
      - 'stride': The number of pixels between adjacent receptive fields in the
        horizontal and vertical directions.
      - 'pad': The number of pixels that will be used to zero-pad the input.

    During padding, 'pad' zeros should be placed symmetrically (i.e equally on both sides)
    along the height and width axes of the input. Be careful not to modfiy the original
    input x directly.

    Returns a tuple of:
    - out: Output data, of shape (N, F, H', W') where H' and W' are given by
      H' = 1 + (H + 2 * pad - HH) / stride
      W' = 1 + (W + 2 * pad - WW) / stride
    - cache: (x, w, b, conv_param)
    """
    out = None
    ###########################################################################
    # TODO: Implement the convolutional forward pass.                         #
    # Hint: you can use the function np.pad for padding.                      #
    ###########################################################################
    # ​**​*​**START OF YOUR CODE*​**​**
    # 获取卷积参数
    stride = conv_param.get('stride', 1)
    pad = conv_param.get('pad', 0)
    
    # 获取输入和权重的维度
    N, C, H, W = x.shape
    F, _, HH, WW = w.shape
    
    # 计算输出尺寸
    H_out = 1 + (H + 2 * pad - HH) // stride
    W_out = 1 + (W + 2 * pad - WW) // stride
    
    # 应用对称零填充
    x_padded = np.pad(x, ((0, 0), (0, 0), (pad, pad), (pad, pad)), mode='constant')
    
    # 初始化输出
    out = np.zeros((N, F, H_out, W_out))
    
    # 执行卷积操作
    for n in range(N):  # 遍历每个样本
        for f in range(F):  # 遍历每个过滤器
            for i in range(H_out):  # 遍历输出高度
                for j in range(W_out):  # 遍历输出宽度
                    # 计算感受野位置
                    h_start = i * stride
                    w_start = j * stride
                    h_end = h_start + HH
                    w_end = w_start + WW
                    
                    # 提取输入块并应用卷积
                    input_patch = x_padded[n, :, h_start:h_end, w_start:w_end]
                    out[n, f, i, j] = np.sum(input_patch * w[f]) + b[f]
    # ​**​*​**END OF YOUR CODE*​**​**
    cache = (x, w, b, conv_param)
    return out, cache


def conv_backward_naive(dout, cache):
    """A naive implementation of the backward pass for a convolutional layer.

    Inputs:
    - dout: Upstream derivatives, of shape (N, F, H', W') 
    - cache: A tuple of (x, w, b, conv_param) as in conv_forward_naive

    Returns a tuple of:
    - dx: Gradient with respect to x, of shape (N, C, H, W)
    - dw: Gradient with respect to w, of shape (F, C, HH, WW)
    - db: Gradient with respect to b, of shape (F,)
    """
    dx, dw, db = None, None, None
    ###########################################################################
    # TODO: Implement the convolutional backward pass.                        #
    ###########################################################################
    # ​**​*​**START OF YOUR CODE*​**​**
    # 获取前向传播的缓存数据
    x, w, b, conv_param = cache
    stride = conv_param['stride']
    pad = conv_param['pad']
    
    # 获取维度信息
    N, C, H, W = x.shape
    F, _, HH, WW = w.shape
    _, _, H_out, W_out = dout.shape
    
    # 初始化梯度
    dx = np.zeros_like(x)
    dw = np.zeros_like(w)
    db = np.zeros_like(b)
    
    # 应用对称零填充
    x_padded = np.pad(x, ((0, 0), (0, 0), (pad, pad), (pad, pad)), mode='constant')
    dx_padded = np.pad(dx, ((0, 0), (0, 0), (pad, pad), (pad, pad)), mode='constant')
    
    # 计算bias梯度
    for f in range(F):
        db[f] = np.sum(dout[:, f, :, :])
    
    # 计算权重的梯度
    for n in range(N):
        for f in range(F):
            for i in range(H_out):
                for j in range(W_out):
                    h_start = i * stride
                    w_start = j * stride
                    h_end = h_start + HH
                    w_end = w_start + WW
                    
                    # 计算dw
                    input_patch = x_padded[n, :, h_start:h_end, w_start:w_end]
                    dw[f] += input_patch * dout[n, f, i, j]
                    
                    # 计算dx
                    dx_padded[n, :, h_start:h_end, w_start:w_end] += w[f] * dout[n, f, i, j]
    
    # 移除填充
    if pad > 0:
        dx = dx_padded[:, :, pad:-pad, pad:-pad]
    else:
        dx = dx_padded
    # ​**​*​**END OF YOUR CODE*​**​**
    return dx, dw, db


def max_pool_forward_naive(x, pool_param):
    """A naive implementation of the forward pass for a max-pooling layer.

    Inputs:
    - x: Input data, of shape (N, C, H, W)
    - pool_param: dictionary with the following keys:
      - 'pool_height': The height of each pooling region
      - 'pool_width': The width of each pooling region
      - 'stride': The distance between adjacent pooling regions

    No padding is necessary here, eg you can assume:
      - (H - pool_height) % stride == 0
      - (W - pool_width) % stride == 0

    Returns a tuple of:
    - out: Output data, of shape (N, C, H', W') where H' and W' are given by
      H' = 1 + (H - pool_height) / stride
      W' = 1 + (W - pool_width) / stride
    - cache: (x, pool_param)
    """
    out = None
    ###########################################################################
    # TODO: Implement the max-pooling forward pass                            #
    ###########################################################################
    # ​**​*​**START OF YOUR CODE*​**​**
    # 获取池化参数
    pool_height = pool_param['pool_height']
    pool_width = pool_param['pool_width']
    stride = pool_param['stride']
    
    # 获取输入维度
    N, C, H, W = x.shape
    
    # 计算输出尺寸
    H_out = (H - pool_height) // stride + 1
    W_out = (W - pool_width) // stride + 1
    
    # 初始化输出
    out = np.zeros((N, C, H_out, W_out))
    
    # 执行最大池化
    for n in range(N):  # 遍历每个样本
        for c in range(C):  # 遍历每个通道
            for i in range(H_out):  # 遍历输出高度
                for j in range(W_out):  # 遍历输出宽度
                    # 计算池化区域位置
                    h_start = i * stride
                    w_start = j * stride
                    h_end = h_start + pool_height
                    w_end = w_start + pool_width
                    
                    # 提取输入区域并取最大值
                    pool_region = x[n, c, h_start:h_end, w_start:w_end]
                    out[n, c, i, j] = np.max(pool_region)
    # ​**​*​**END OF YOUR CODE*​**​**
    cache = (x, pool_param)
    return out, cache


def max_pool_backward_naive(dout, cache):
    """A naive implementation of the backward pass for a max-pooling layer.

    Inputs:
    - dout: Upstream derivatives, of shape (N, C, H', W')
    - cache: A tuple of (x, pool_param) as in the forward pass.

    Returns:
    - dx: Gradient with respect to x, of shape (N, C, H, W)
    """
    dx = None
    ###########################################################################
    # TODO: Implement the max-pooling backward pass                           #
    ###########################################################################
    # ​**​*​**START OF YOUR CODE*​**​**
    # 获取前向传播的缓存数据
    x, pool_param = cache
    pool_height = pool_param['pool_height']
    pool_width = pool_param['pool_width']
    stride = pool_param['stride']
    
    # 获取维度信息
    N, C, H, W = x.shape
    _, _, H_out, W_out = dout.shape
    
    # 初始化梯度
    dx = np.zeros_like(x)
    
    # 执行反向传播
    for n in range(N):  # 遍历每个样本
        for c in range(C):  # 遍历每个通道
            for i in range(H_out):  # 遍历输出高度
                for j in range(W_out):  # 遍历输出宽度
                    # 计算池化区域位置
                    h_start = i * stride
                    w_start = j * stride
                    h_end = h_start + pool_height
                    w_end = w_start + pool_width
                    
                    # 提取输入区域
                    pool_region = x[n, c, h_start:h_end, w_start:w_end]
                    
                    # 找到最大值位置
                    max_idx = np.unravel_index(np.argmax(pool_region), pool_region.shape)
                    max_h = h_start + max_idx[0]
                    max_w = w_start + max_idx[1]
                    
                    # 分配梯度
                    dx[n, c, max_h, max_w] += dout[n, c, i, j]
    # ​**​*​**END OF YOUR CODE*​**​**
    return dx

