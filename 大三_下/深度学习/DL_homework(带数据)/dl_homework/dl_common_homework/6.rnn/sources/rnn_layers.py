"""This file defines layer types that are commonly used for recurrent neural networks.
"""

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
    out = x.reshape(x.shape[0], -1).dot(w) + b
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
    dx = dout.dot(w.T).reshape(x.shape)
    dw = x.reshape(x.shape[0], -1).T.dot(dout)
    db = np.sum(dout, axis=0)
    return dx, dw, db


def rnn_step_forward(x, prev_h, Wx, Wh, b):
    """Run the forward pass for a single timestep of a vanilla RNN using a tanh activation function.

    The input data has dimension D, the hidden state has dimension H,
    and the minibatch is of size N.

    Inputs:
    - x: Input data for this timestep, of shape (N, D)
    - prev_h: Hidden state from previous timestep, of shape (N, H)
    - Wx: Weight matrix for input-to-hidden connections, of shape (D, H)
    - Wh: Weight matrix for hidden-to-hidden connections, of shape (H, H)
    - b: Biases of shape (H,)

    Returns a tuple of:
    - next_h: Next hidden state, of shape (N, H)
    - cache: Tuple of values needed for the backward pass.
    """
    next_h, cache = None, None
    ##############################################################################
    # TODO: Implement a single forward step for the vanilla RNN. Store the next  #
    # hidden state and any values you need for the backward pass in the next_h   #
    # and cache variables respectively.                                          #
    ##############################################################################
    # Don't forget tanh!
    # ​**​*​**START OF YOUR CODE*​**​**
    # 计算当前时间步的隐藏状态：next_h = tanh(x * Wx + prev_h * Wh + b)
    affine_input = np.dot(x, Wx)  # (N, H)
    affine_hidden = np.dot(prev_h, Wh)  # (N, H)
    sum_affine = affine_input + affine_hidden + b  # (N, H)
    next_h = np.tanh(sum_affine)  # (N, H)
    
    # 缓存前向传播的中间结果，用于反向传播
    cache = (x, prev_h, Wx, Wh, sum_affine, next_h)
    # ​**​*​**END OF YOUR CODE*​**​**
    return next_h, cache


def rnn_step_backward(dnext_h, cache):
    """Backward pass for a single timestep of a vanilla RNN.

    Inputs:
    - dnext_h: Gradient of loss with respect to next hidden state, of shape (N, H)
    - cache: Cache object from the forward pass

    Returns a tuple of:
    - dx: Gradients of input data, of shape (N, D)
    - dprev_h: Gradients of previous hidden state, of shape (N, H)
    - dWx: Gradients of input-to-hidden weights, of shape (D, H)
    - dWh: Gradients of hidden-to-hidden weights, of shape (H, H)
    - db: Gradients of bias vector, of shape (H,)
    """
    dx, dprev_h, dWx, dWh, db = None, None, None, None, None
    ##############################################################################
    # TODO: Implement the backward pass for a single step of a vanilla RNN.      #
    ##############################################################################
    # ​**​*​**START OF YOUR CODE*​**​**
    # 从缓存中获取前向传播的中间结果
    x, prev_h, Wx, Wh, sum_affine, next_h = cache
    
    # 计算tanh激活函数的梯度：dtanh = (1 - next_h**2) * dnext_h
    dtanh = (1 - next_h**2) * dnext_h
    
    # 计算输入梯度：dx = dtanh * Wx^T
    dx = np.dot(dtanh, Wx.T)
    
    # 计算前一隐藏状态梯度：dprev_h = dtanh * Wh^T
    dprev_h = np.dot(dtanh, Wh.T)
    
    # 计算权重梯度：dWx = x^T * dtanh, dWh = prev_h^T * dtanh
    dWx = np.dot(x.T, dtanh)
    dWh = np.dot(prev_h.T, dtanh)
    
    # 计算偏置梯度：db = sum(dtanh, axis=0)
    db = np.sum(dtanh, axis=0)
    # ​**​*​**END OF YOUR CODE*​**​**
    return dx, dprev_h, dWx, dWh, db


def rnn_forward(x, h0, Wx, Wh, b):
    """Run a vanilla RNN forward on an entire sequence of data.
    
    We assume an input sequence composed of T vectors, each of dimension D. The RNN uses a hidden
    size of H, and we work over a minibatch containing N sequences. After running the RNN forward,
    we return the hidden states for all timesteps.

    Inputs:
    - x: Input data for the entire timeseries, of shape (N, T, D)
    - h0: Initial hidden state, of shape (N, H)
    - Wx: Weight matrix for input-to-hidden connections, of shape (D, H)
    - Wh: Weight matrix for hidden-to-hidden connections, of shape (H, H)
    - b: Biases of shape (H,)

    Returns a tuple of:
    - h: Hidden states for the entire timeseries, of shape (N, T, H)
    - cache: Values needed in the backward pass
    """
    h, cache = None, None
    ##############################################################################
    # TODO: Implement forward pass for a vanilla RNN running on a sequence of    #
    # input data. You should use the rnn_step_forward function that you defined  #
    # above. You can use a for loop to help compute the forward pass.            #
    ##############################################################################
    # ​**​*​**START OF YOUR CODE*​**​**
    N, T, D = x.shape
    H = h0.shape[1]
    
    # 初始化隐藏状态矩阵
    h = np.zeros((N, T, H))
    prev_h = h0
    cache_list = []
    
    # 遍历每个时间步
    for t in range(T):
        # 获取当前时间步的输入
        x_t = x[:, t, :]
        
        # 执行单步前向传播
        next_h, cache_step = rnn_step_forward(x_t, prev_h, Wx, Wh, b)
        
        # 存储当前时间步的隐藏状态
        h[:, t, :] = next_h
        
        # 更新前一隐藏状态
        prev_h = next_h
        
        # 保存缓存
        cache_list.append(cache_step)
    
    # 缓存包含所有时间步的信息
    cache = (x, h0, Wx, Wh, b, cache_list)
    # ​**​*​**END OF YOUR CODE*​**​**
    return h, cache


def rnn_backward(dh, cache):
    """Compute the backward pass for a vanilla RNN over an entire sequence of data.

    Inputs:
    - dh: Upstream gradients of all hidden states, of shape (N, T, H)
    
    NOTE: 'dh' contains the upstream gradients produced by the 
    individual loss functions at each timestep, *not* the gradients
    being passed between timesteps (which you'll have to compute yourself
    by calling rnn_step_backward in a loop).

    Returns a tuple of:
    - dx: Gradient of inputs, of shape (N, T, D)
    - dh0: Gradient of initial hidden state, of shape (N, H)
    - dWx: Gradient of input-to-hidden weights, of shape (D, H)
    - dWh: Gradient of hidden-to-hidden weights, of shape (H, H)
    - db: Gradient of biases, of shape (H,)
    """
    dx, dh0, dWx, dWh, db = None, None, None, None, None
    ##############################################################################
    # TODO: Implement the backward pass for a vanilla RNN running an entire      #
    # sequence of data. You should use the rnn_step_backward function that you   #
    # defined above. You can use a for loop to help compute the backward pass.   #
    ##############################################################################
    # ​**​*​**START OF YOUR CODE*​**​**
    # 从缓存中获取前向传播信息
    x, h0, Wx, Wh, b, cache_list = cache
    N, T, H = dh.shape
    D = x.shape[2]
    
    # 初始化梯度
    dx = np.zeros_like(x)
    dprev_h = np.zeros_like(h0)
    dWx = np.zeros_like(Wx)
    dWh = np.zeros_like(Wh)
    db = np.zeros_like(b)
    
    # 初始化下一个时间步的梯度
    dnext_h = np.zeros((N, H))
    
    # 反向遍历时间步
    for t in range(T-1, -1, -1):
        # 当前时间步的梯度 = 来自输出的梯度 + 来自下一个时间步的梯度
        dcurrent = dh[:, t, :] + dnext_h
        
        # 执行单步反向传播
        dx_t, dprev_h, dWx_t, dWh_t, db_t = rnn_step_backward(dcurrent, cache_list[t])
        
        # 保存输入梯度
        dx[:, t, :] = dx_t
        
        # 累加权重梯度（所有时间步共享权重）
        dWx += dWx_t
        dWh += dWh_t
        db += db_t
        
        # 设置下一个时间步的梯度
        dnext_h = dprev_h
    
    # 初始隐藏状态的梯度
    dh0 = dnext_h
    # ​**​*​**END OF YOUR CODE*​**​**
    return dx, dh0, dWx, dWh, db


def word_embedding_forward(x, W):
    """Forward pass for word embeddings.
    
    We operate on minibatches of size N where
    each sequence has length T. We assume a vocabulary of V words, assigning each
    word to a vector of dimension D.

    Inputs:
    - x: Integer array of shape (N, T) giving indices of words. Each element idx
      of x muxt be in the range 0 <= idx < V.
    - W: Weight matrix of shape (V, D) giving word vectors for all words.

    Returns a tuple of:
    - out: Array of shape (N, T, D) giving word vectors for all input words.
    - cache: Values needed for the backward pass
    """
    out, cache = None, None
    ##############################################################################
    # TODO: Implement the forward pass for word embeddings.                      #
    #                                                                            #
    # HINT: This can be done in one line using NumPy's array indexing.           #
    ##############################################################################
    # ​**​*​**START OF YOUR CODE*​**​**
    # 使用索引从权重矩阵W中选取对应的词向量
    out = W[x]  # (N, T, D)
    
    # 缓存输入和权重矩阵形状
    cache = (x, W.shape)
    # ​**​*​**END OF YOUR CODE*​**​**
    return out, cache


def word_embedding_backward(dout, cache):
    """Backward pass for word embeddings.
    
    We cannot back-propagate into the words
    since they are integers, so we only return gradient for the word embedding
    matrix.

    HINT: Look up the function np.add.at

    Inputs:
    - dout: Upstream gradients of shape (N, T, D)
    - cache: Values from the forward pass

    Returns:
    - dW: Gradient of word embedding matrix, of shape (V, D)
    """
    dW = None
    ##############################################################################
    # TODO: Implement the backward pass for word embeddings.                     #
    #                                                                            #
    # Note that words can appear more than once in a sequence.                   #
    # HINT: Look up the function np.add.at                                       #
    ##############################################################################
    # ​**​*​**START OF YOUR CODE*​**​**
    x, W_shape = cache
    V, D = W_shape
    
    # 初始化权重梯度
    dW = np.zeros((V, D))
    
    # 使用np.add.at高效累加梯度（处理同一词多次出现的情况）
    np.add.at(dW, x, dout)
    # ​**​*​**END OF YOUR CODE*​**​**
    return dW


def sigmoid(x):
    """A numerically stable version of the logistic sigmoid function."""
    pos_mask = x >= 0
    neg_mask = x < 0
    z = np.zeros_like(x)
    z[pos_mask] = np.exp(-x[pos_mask])
    z[neg_mask] = np.exp(x[neg_mask])
    top = np.ones_like(x)
    top[neg_mask] = z[neg_mask]
    return top / (1 + z)


def lstm_step_forward(x, prev_h, prev_c, Wx, Wh, b):
    """Forward pass for a single timestep of an LSTM.

    The input data has dimension D, the hidden state has dimension H, and we use
    a minibatch size of N.

    Note that a sigmoid() function has already been provided for you in this file.

    Inputs:
    - x: Input data, of shape (N, D)
    - prev_h: Previous hidden state, of shape (N, H)
    - prev_c: previous cell state, of shape (N, H)
    - Wx: Input-to-hidden weights, of shape (D, 4H)
    - Wh: Hidden-to-hidden weights, of shape (H, 4H)
    - b: Biases, of shape (4H,)

    Returns a tuple of:
    - next_h: Next hidden state, of shape (N, H)
    - next_c: Next cell state, of shape (N, H)
    - cache: Tuple of values needed for backward pass.
    """
    next_h, next_c, cache = None, None, None
    #############################################################################
    # TODO: Implement the forward pass for a single timestep of an LSTM.        #
    # You may want to use the numerically stable sigmoid implementation above.  #
    #############################################################################
    # ​**​*​**START OF YOUR CODE*​**​**
    # 获取输入和隐藏状态的维度
    N, D = x.shape
    H = prev_h.shape[1]
    
    # 计算门控和候选状态
    affine = np.dot(x, Wx) + np.dot(prev_h, Wh) + b
    
    # 分割affine得到输入门(i)、遗忘门(f)、输出门(o)和候选细胞状态(ct)
    i = sigmoid(affine[:, 0:H])
    f = sigmoid(affine[:, H:2*H])
    o = sigmoid(affine[:, 2*H:3*H])
    ct = np.tanh(affine[:, 3*H:4*H])
    
    # 更新细胞状态：next_c = f * prev_c + i * ct
    next_c = f * prev_c + i * ct
    
    # 计算下一隐藏状态：next_h = o * tanh(next_c)
    next_h = o * np.tanh(next_c)
    
    # 缓存中间结果
    cache = (x, prev_h, prev_c, Wx, Wh, i, f, o, ct, next_c, next_h)
    # ​**​*​**END OF YOUR CODE*​**​**

    return next_h, next_c, cache


def lstm_step_backward(dnext_h, dnext_c, cache):
    """Backward pass for a single timestep of an LSTM.

    Inputs:
    - dnext_h: Gradients of next hidden state, of shape (N, H)
    - dnext_c: Gradients of next cell state, of shape (N, H)
    - cache: Values from the forward pass

    Returns a tuple of:
    - dx: Gradient of input data, of shape (N, D)
    - dprev_h: Gradient of previous hidden state, of shape (N, H)
    - dprev_c: Gradient of previous cell state, of shape (N, H)
    - dWx: Gradient of input-to-hidden weights, of shape (D, 4H)
    - dWh: Gradient of hidden-to-hidden weights, of shape (H, 4H)
    - db: Gradient of biases, of shape (4H,)
    """
    dx, dprev_h, dprev_c, dWx, dWh, db = None, None, None, None, None, None
    #############################################################################
    # TODO: Implement the backward pass for a single timestep of an LSTM.       #
    #                                                                           #
    # HINT: For sigmoid and tanh you can compute local derivatives in terms of  #
    # the output value from the nonlinearity.                                   #
    #############################################################################
    # ​**​*​**START OF YOUR CODE*​**​**
    # 从缓存中获取中间结果
    x, prev_h, prev_c, Wx, Wh, i, f, o, ct, next_c, next_h = cache
    
    # 计算tanh(next_c)的梯度
    dtanh_next_c = o * dnext_h
    dnext_c += (1 - np.tanh(next_c)**2) * dtanh_next_c
    
    # 计算细胞状态梯度
    dprev_c = f * dnext_c
    
    # 计算候选状态梯度
    dct = i * dnext_c
    di = ct * dnext_c
    
    # 计算门控梯度
    df = prev_c * dnext_c
    do = np.tanh(next_c) * dnext_h
    
    # 计算输入门、遗忘门、输出门和候选状态的局部梯度
    di_input = i * (1 - i) * di
    df_input = f * (1 - f) * df
    do_input = o * (1 - o) * do
    dct_input = (1 - ct**2) * dct
    
    # 合并所有梯度
    daffine = np.hstack((di_input, df_input, do_input, dct_input))
    
    # 计算参数梯度
    dx = np.dot(daffine, Wx.T)
    dprev_h = np.dot(daffine, Wh.T)
    dWx = np.dot(x.T, daffine)
    dWh = np.dot(prev_h.T, daffine)
    db = np.sum(daffine, axis=0)
    # ​**​*​**END OF YOUR CODE*​**​**

    return dx, dprev_h, dprev_c, dWx, dWh, db


def lstm_forward(x, h0, Wx, Wh, b):
    """Forward pass for an LSTM over an entire sequence of data.
    
    We assume an input sequence composed of T vectors, each of dimension D. The LSTM uses a hidden
    size of H, and we work over a minibatch containing N sequences. After running the LSTM forward,
    we return the hidden states for all timesteps.

    Note that the initial cell state is passed as input, but the initial cell state is set to zero.
    Also note that the cell state is not returned; it is an internal variable to the LSTM and is not
    accessed from outside.

    Inputs:
    - x: Input data of shape (N, T, D)
    - h0: Initial hidden state of shape (N, H)
    - Wx: Weights for input-to-hidden connections, of shape (D, 4H)
    - Wh: Weights for hidden-to-hidden connections, of shape (H, 4H)
    - b: Biases of shape (4H,)

    Returns a tuple of:
    - h: Hidden states for all timesteps of all sequences, of shape (N, T, H)
    - cache: Values needed for the backward pass.
    """
    h, cache = None, None
    #############################################################################
    # TODO: Implement the forward pass for an LSTM over an entire timeseries.   #
    # You should use the lstm_step_forward function that you just defined.      #
    #############################################################################
    # ​**​*​**START OF YOUR CODE*​**​**
    N, T, D = x.shape
    H = h0.shape[1]
    
    # 初始化隐藏状态和细胞状态
    h = np.zeros((N, T, H))
    prev_h = h0
    prev_c = np.zeros_like(h0)  # 初始细胞状态为零
    cache_list = []
    
    # 遍历每个时间步
    for t in range(T):
        # 获取当前时间步的输入
        x_t = x[:, t, :]
        
        # 执行LSTM单步前向传播
        next_h, next_c, cache_step = lstm_step_forward(x_t, prev_h, prev_c, Wx, Wh, b)
        
        # 存储当前时间步的隐藏状态
        h[:, t, :] = next_h
        
        # 更新前一隐藏状态和细胞状态
        prev_h = next_h
        prev_c = next_c
        
        # 保存缓存
        cache_list.append(cache_step)
    
    # 缓存包含所有时间步的信息
    cache = (x, h0, Wx, Wh, b, cache_list)
    # ​**​*​**END OF YOUR CODE*​**​**

    return h, cache


def lstm_backward(dh, cache):
    """Backward pass for an LSTM over an entire sequence of data.

    Inputs:
    - dh: Upstream gradients of hidden states, of shape (N, T, H)
    - cache: Values from the forward pass

    Returns a tuple of:
    - dx: Gradient of input data of shape (N, T, D)
    - dh0: Gradient of initial hidden state of shape (N, H)
    - dWx: Gradient of input-to-hidden weight matrix of shape (D, 4H)
    - dWh: Gradient of hidden-to-hidden weight matrix of shape (H, 4H)
    - db: Gradient of biases, of shape (4H,)
    """
    dx, dh0, dWx, dWh, db = None, None, None, None, None
    #############################################################################
    # TODO: Implement the backward pass for an LSTM over an entire timeseries.  #
    # You should use the lstm_step_backward function that you just defined.     #
    #############################################################################
    # ​**​*​**START OF YOUR CODE*​**​**
    # 从缓存中获取前向传播信息
    x, h0, Wx, Wh, b, cache_list = cache
    N, T, H = dh.shape
    D = x.shape[2]
    
    # 初始化梯度
    dx = np.zeros_like(x)
    dprev_h = np.zeros_like(h0)
    dprev_c = np.zeros_like(dprev_h)
    dWx = np.zeros_like(Wx)
    dWh = np.zeros_like(Wh)
    db = np.zeros_like(b)
    
    # 初始化下一个时间步的梯度
    dnext_h = np.zeros((N, H))
    dnext_c = np.zeros((N, H))
    
    # 反向遍历时间步
    for t in range(T-1, -1, -1):
        # 当前时间步的隐藏状态梯度
        dh_t = dh[:, t, :] + dnext_h
        
        # 执行LSTM单步反向传播
        dx_t, dprev_h, dprev_c, dWx_t, dWh_t, db_t = lstm_step_backward(
            dh_t, dnext_c, cache_list[t]
        )
        
        # 保存输入梯度
        dx[:, t, :] = dx_t
        
        # 累加权重梯度（所有时间步共享权重）
        dWx += dWx_t
        dWh += dWh_t
        db += db_t
        
        # 设置下一个时间步的梯度
        dnext_h = dprev_h
        dnext_c = dprev_c
    
    # 初始隐藏状态的梯度
    dh0 = dprev_h
    # ​**​*​**END OF YOUR CODE*​**​**

    return dx, dh0, dWx, dWh, db


def temporal_affine_forward(x, w, b):
    """Forward pass for a temporal affine layer.
    
    The input is a set of D-dimensional
    vectors arranged into a minibatch of N timeseries, each of length T. We use
    an affine function to transform each of those vectors into a new vector of
    dimension M.

    Inputs:
    - x: Input data of shape (N, T, D)
    - w: Weights of shape (D, M)
    - b: Biases of shape (M,)

    Returns a tuple of:
    - out: Output data of shape (N, T, M)
    - cache: Values needed for the backward pass
    """
    N, T, D = x.shape
    M = b.shape[0]
    out = x.reshape(N * T, D).dot(w).reshape(N, T, M) + b
    cache = x, w, b, out
    return out, cache


def temporal_affine_backward(dout, cache):
    """Backward pass for temporal affine layer.

    Input:
    - dout: Upstream gradients of shape (N, T, M)
    - cache: Values from forward pass

    Returns a tuple of:
    - dx: Gradient of input, of shape (N, T, D)
    - dw: Gradient of weights, of shape (D, M)
    - db: Gradient of biases, of shape (M,)
    """
    x, w, b, out = cache
    N, T, D = x.shape
    M = b.shape[0]

    dx = dout.reshape(N * T, M).dot(w.T).reshape(N, T, D)
    dw = dout.reshape(N * T, M).T.dot(x.reshape(N * T, D)).T
    db = dout.sum(axis=(0, 1))

    return dx, dw, db


def temporal_softmax_loss(x, y, mask, verbose=False):
    """A temporal version of softmax loss for use in RNNs.
    
    We assume that we are making predictions over a vocabulary of size V for each timestep of a
    timeseries of length T, over a minibatch of size N. The input x gives scores for all vocabulary
    elements at all timesteps, and y gives the indices of the ground-truth element at each timestep.
    We use a cross-entropy loss at each timestep, summing the loss over all timesteps and averaging
    across the minibatch.

    As an additional complication, we may want to ignore the model output at some timesteps, since
    sequences of different length may have been combined into a minibatch and padded with NULL
    tokens. The optional mask argument tells us which elements should contribute to the loss.

    Inputs:
    - x: Input scores, of shape (N, T, V)
    - y: Ground-truth indices, of shape (N, T) where each element is in the range
         0 <= y[i, t] < V
    - mask: Boolean array of shape (N, T) where mask[i, t] tells whether or not
      the scores at x[i, t] should contribute to the loss.

    Returns a tuple of:
    - loss: Scalar giving loss
    - dx: Gradient of loss with respect to scores x.
    """

    N, T, V = x.shape

    x_flat = x.reshape(N * T, V)
    y_flat = y.reshape(N * T)
    mask_flat = mask.reshape(N * T)

    probs = np.exp(x_flat - np.max(x_flat, axis=1, keepdims=True))
    probs /= np.sum(probs, axis=1, keepdims=True)
    loss = -np.sum(mask_flat * np.log(probs[np.arange(N * T), y_flat])) / N
    dx_flat = probs.copy()
    dx_flat[np.arange(N * T), y_flat] -= 1
    dx_flat /= N
    dx_flat *= mask_flat[:, None]

    if verbose:
        print("dx_flat: ", dx_flat.shape)

    dx = dx_flat.reshape(N, T, V)

    return loss, dx
