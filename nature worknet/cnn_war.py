import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data

mnist = input_data.read_data_sets('MNIST_data', one_hot=True)

def weight_variable(shape):
    initial = tf.truncated_normal(shape, stddev=0.1)
    return tf.Variable(initial)

def biases_variable(shape):
    initial = tf.constant(0.1, shape = shape)
    return tf.Variable(initial)

def conv2d(x ,W):
    #stride = [1,x_movement, y_movement ,1]
    #have must stride[0] and stride[3] = 1

    return tf.nn.conv2d(x, W, strides = [1,1,1,1], padding = 'SAME')

def max_pool_2x2(x):
    # ksize  [1,pool_op_length(池化倍数，这里设置为二),pool_op_width,1]
    # Must have ksize[0] = ksize[3] = 1
    #stride = [1,x_movement, y_movement ,1]
    #have must stride[0] and stride[3] = 1
    return tf.nn.max_pool(x, ksize = [1,2,2,1], strides = [1,2,2,1], padding = 'SAME')

#占位符
xs = tf.placeholder(tf.float32,[None,784])
ys = tf.placeholder(tf.float32,[None,10])
keep_prob = tf.placeholder(tf.float32)
x_image = tf.reshape(xs, [-1,28,28,1])

#卷积层第一层
W_conv1 = weight_variable([5,5,1,32])
b_conv1 = biases_variable([32])
h_conv1 = tf.nn.relu(conv2d(x_image, W_conv1) + b_conv1)
h_pool = max_pool_2x2(h_conv1)

#卷积层第二层
W_conv2 = weight_variable([5,5,32,64])
b_conv2 = biases_variable([64])
h_conv2 = tf.nn.relu(conv2d(h_pool, W_conv2) + b_conv2)
h_pool2 = max_pool_2x2(h_conv2)           # output size 7x7x64

##flat h_pool2##
h_pool2_flat = tf.reshape(h_pool2, [-1,7*7*64])

## fc1 layer ## 输入输出以及隐藏层
W_fc1 = weight_variable([7*7*64,1024])
b_fc1 = biases_variable([1024])
h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, W_fc1) + b_fc1)
h_fcl_drop = tf.nn.dropout(h_fc1, keep_prob)

#fc2 layer 隐藏层及输出层
W_fc2 = weight_variable([1024,10])
b_fc2 = biases_variable([10])
prediction = tf.nn.softmax(tf.matmul(h_fcl_drop, W_fc2) + b_fc2)

cross_entropy = tf.reduce_mean(-tf.reduce_sum(ys * tf.log(prediction),reduction_indices = [1])) #损失函数
train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy) #优化器的选择

init = tf.global_variables_initializer()
sess = tf.Session()
sess.run(init)


def compute_accuracy(v_xs, v_ys):
    global prediction
    y_pre = sess.run(prediction, feed_dict={xs: v_xs, keep_prob: 1})  # 使用测试集得到的结果
    correct_prediction = tf.equal(tf.argmax(y_pre, 1), tf.argmax(v_ys, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
    result = sess.run(accuracy, feed_dict={xs: v_xs, ys: v_ys, keep_prob: 1})
    return result



for i in range(1000):
    batch_xs, batch_ys = mnist.train.next_batch(10)
    sess.run(train_step, feed_dict = {xs:batch_xs, ys:batch_ys,keep_prob:0.5})
    if i%50 == 0:
        print(compute_accuracy (mnist.test.images, mnist.test.labels))














