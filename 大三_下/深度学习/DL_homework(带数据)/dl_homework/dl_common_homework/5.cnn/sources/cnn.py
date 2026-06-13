from builtins import object
import numpy as np

from .layers_cnn import *
from .fast_layers import *


class ThreeLayerConvNet(object):
    """
    A three-layer convolutional network with the following architecture:

    conv - relu - 2x2 max pool - affine - relu - affine - softmax

    The network operates on minibatches of data that have shape (N, C, H, W)
    consisting of N images, each with height H and width W and with C input
    channels.
    """

    def __init__(
        self,
        input_dim=(3, 32, 32),
        num_filters=32,
        filter_size=7,
        hidden_dim=100,
        num_classes=10,
        weight_scale=1e-3,
        reg=0.0,
        dtype=np.float32,
    ):
        """
        Initialize a new network.

        Inputs:
        - input_dim: Tuple (C, H, W) giving size of input data
        - num_filters: Number of filters to use in the convolutional layer
        - filter_size: Width/height of filters to use in the convolutional layer
        - hidden_dim: Number of units to use in the fully-connected hidden layer
        - num_classes: Number of scores to produce from the final affine layer.
        - weight_scale: Scalar giving standard deviation for random initialization
          of weights.
        - reg: Scalar giving L2 regularization strength
        - dtype: numpy datatype to use for computation.
        """
        self.params = {}
        self.reg = reg
        self.dtype = dtype

        ############################################################################
        # TODO: Initialize weights and biases for the three-layer convolutional    #
        # network. Weights should be initialized from a Gaussian centered at 0.0   #
        # with standard deviation equal to weight_scale; biases should be          #
        # initialized to zero. All weights and biases should be stored in the      #
        #  dictionary self.params. Store weights and biases for the convolutional  #
        # layer using the keys 'W1' and 'b1'; use keys 'W2' and 'b2' for the       #
        # weights and biases of the hidden affine layer, and keys 'W3' and 'b3'    #
        # for the weights and biases of the output affine layer.                   #
        #                                                                          #
        # IMPORTANT: For this assignment, you can assume that the padding          #
        # and stride of the first convolutional layer are chosen so that           #
        # **the width and height of the input are preserved**. Take a look at      #
        # the start of the loss() function to see how that happens.                #
        ############################################################################
        # conv - relu - 2x2 max pool - affine - relu - affine - softmax
        # ​**​*​**START OF YOUR CODE*​**​**
        # 获取输入维度
        C, H, W = input_dim
        
        # 初始化卷积层参数
        self.params['W1'] = np.random.randn(num_filters, C, filter_size, filter_size) * weight_scale
        self.params['b1'] = np.zeros(num_filters)
        
        # 计算池化后尺寸 (2x2 池化，步长为2)
        H_pool = H // 2
        W_pool = W // 2
        
        # 初始化第一个全连接层参数
        self.params['W2'] = np.random.randn(num_filters * H_pool * W_pool, hidden_dim) * weight_scale
        self.params['b2'] = np.zeros(hidden_dim)
        
        # 初始化第二个全连接层参数
        self.params['W3'] = np.random.randn(hidden_dim, num_classes) * weight_scale
        self.params['b3'] = np.zeros(num_classes)
        # ​**​*​**END OF YOUR CODE*​**​**
        for k, v in self.params.items():
            self.params[k] = v.astype(dtype)

    def loss(self, X, y=None):
        """
        Evaluate loss and gradient for the three-layer convolutional network.

        Input / output: Same API as TwoLayerNet.
        """
        W1, b1 = self.params["W1"], self.params["b1"]
        W2, b2 = self.params["W2"], self.params["b2"]
        W3, b3 = self.params["W3"], self.params["b3"]

        # pass conv_param to the forward pass for the convolutional layer
        # Padding and stride chosen to preserve the input spatial size
        filter_size = W1.shape[2]
        conv_param = {"stride": 1, "pad": (filter_size - 1) // 2}

        # pass pool_param to the forward pass for the max-pooling layer
        pool_param = {"pool_height": 2, "pool_width": 2, "stride": 2}

        scores = None
        ############################################################################
        # TODO: Implement the forward pass for the three-layer convolutional net,  #
        # computing the class scores for X and storing them in the scores          #
        # variable.                                                                #
        #                                                                          #
        # Remember you can use the functions defined in cs231n/fast_layers.py and  #
        # cs231n/layer_utils.py in your implementation (already imported).         #
        ############################################################################
        # conv - relu - 2x2 max pool - affine - relu - affine - softmax
        # ​**​*​**START OF YOUR CODE*​**​**
        # 卷积层前向传播
        conv_out, cache_conv = conv_forward_fast(X, W1, b1, conv_param)
        
        # ReLU激活
        relu1_out, cache_relu1 = relu_forward(conv_out)
        
        # 最大池化层前向传播
        pool_out, cache_pool = max_pool_forward_fast(relu1_out, pool_param)
        
        # 记录池化层输出形状（用于反向传播）
        pool_shape = pool_out.shape
        
        # 展平池化层输出
        affine1_in = pool_out.reshape(pool_shape[0], -1)
        
        # 第一个全连接层前向传播
        affine1_out, cache_affine1 = affine_forward(affine1_in, W2, b2)
        
        # ReLU激活
        relu2_out, cache_relu2 = relu_forward(affine1_out)
        
        # 第二个全连接层前向传播
        scores, cache_affine2 = affine_forward(relu2_out, W3, b3)
        # ​**​*​**END OF YOUR CODE*​**​**

        if y is None:
            return scores

        loss, grads = 0, {}
        #############################################################################
        # TODO: Implement the backward pass for the three-layer convolutional net,  #
        # storing the loss and gradients in the loss and grads variables. Compute   #
        # data loss using softmax, and make sure that grads[k] holds the gradients  #
        # for self.params[k]. Don't forget to add L2 regularization, which includes #
        # a factor of 0.5 to simplify the expression for the gradient.              #
        #############################################################################
        # ​**​*​**START OF YOUR CODE*​**​**
        # 计算softmax损失
        loss, dout = softmax_loss(scores, y)
        
        # 添加L2正则化项
        loss += 0.5 * self.reg * (np.sum(W1**2) + np.sum(W2**2) + np.sum(W3**2))
        
        # 第二个全连接层反向传播
        dout, dW3, db3 = affine_backward(dout, cache_affine2)
        
        # 第一个全连接层的ReLU反向传播
        dout = relu_backward(dout, cache_relu2)
        
        # 第一个全连接层反向传播
        dout, dW2, db2 = affine_backward(dout, cache_affine1)
        
        # 将梯度重塑为池化层输出的形状
        dout = dout.reshape(pool_shape)
        
        # 最大池化层反向传播
        dout = max_pool_backward_fast(dout, cache_pool)
        
        # 卷积层的ReLU反向传播
        dout = relu_backward(dout, cache_relu1)
        
        # 卷积层反向传播
        dout, dW1, db1 = conv_backward_fast(dout, cache_conv)
        
        # 添加正则化项的梯度
        dW1 += self.reg * W1
        dW2 += self.reg * W2
        dW3 += self.reg * W3
        
        # 保存梯度
        grads = {'W1': dW1, 'b1': db1, 'W2': dW2, 'b2': db2, 'W3': dW3, 'b3': db3}
        # ​**​*​**END OF YOUR CODE*​**​**
        return loss, grads
