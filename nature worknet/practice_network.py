import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

#结构
#creat data
x_data = np.random.rand(100).astype(np.float32)
y_data = x_data * 0.1 + 0.3


###creat tensfloat structure state###
Weights = tf.Variable(tf.random_uniform([1],-1.0,1.0)) #Weights could be matrix/array,Variable is Weights' 参数变量
biases = tf.Variable(tf.zeros([1]))#初始值为零

y = Weights*x_data + biases

loss = tf.reduce_mean(tf.square(y - y_data)) #损失函数 回归问题常用的为均方差损失函数
optimizer = tf.train.GradientDescentOptimizer(0.5)#优化器，有很多种优化器， 0.5为学习效率，一般为小于一的数
trian = optimizer.minimize(loss)#优化损失函数，减少误差，每步都要做

init = tf.initialize_all_variables()
###creat tensfloat structure state###

sess = tf.Session()#
sess.run(init)#very important

for step in range(201):
    sess.run(trian)
    if step % 20==0:
        print(step,sess.run(Weights),sess.run(biases))

#会话
matrix1 = tf.constant([[3,3]])
matrix2 = tf.constant([[2],[2]])
product = tf.matmul(matrix1,matrix2)

# sess = tf.Session()
# result = sess.run(product)
# print(result)
# sess.close()
with tf.Session() as sess:
    result2 = sess.run(product)
    print(result2)


input1 = tf.placeholder(tf.float32)
input2 = tf.placeholder(tf.float32)
output = tf.multiply(input1,input2)

with tf.Session() as sess:
    print(sess.run(output,feed_dict = {input1: [7] ,input2: [2] }))

#激励函数使用及 添加层
def add_layer(inputs,in_size,out_size,activation_function = None):
    Weights = tf.Variable(tf.random_normal([in_size,out_size]))#matrixs'row and col
    biases = tf.Variable(tf.zeros([1,out_size]) + 0.1)#recommend not be zero,so add 0.1
    Wx_plus_b = tf.matmul(inputs,Weights) + biases
    if activation_function is None:
        outputs = Wx_plus_b
    else:
        outputs = activation_function(Wx_plus_b)
    return outputs

#构建神经网络
x_data = np.linspace(-1,1,300)[:,np.newaxis] #300行，
noise = np.random.normal(0,0.05,x_data.shape)
y_data = np.square(x_data) - 0.5 + noise

xs = tf.placeholder(tf.float32,[None,1])
ys = tf.placeholder(tf.float32,[None,1])
l1 = add_layer(xs,1,10,activation_function = tf.nn.relu)
prediction = add_layer(l1,10,1,activation_function = None)

loss = tf.reduce_mean(tf.reduce_sum(tf.square(ys - prediction),reduction_indices = [1]))
train_step = tf.train.GradientDescentOptimizer(0.1).minimize(loss)#学习效率为0.1，

init = tf.global_variables_initializer()
sess = tf.Session()
sess.run(init)

fig = plt.figure()
ax = fig.add_subplot(1,1,1)
ax.scatter(x_data,y_data)
plt.ion()#使图持续动起来
plt.show()

for i in range(1000):
    sess.run(train_step,feed_dict = {xs:x_data,ys:y_data})
    if i%50 == 0:
        #print(sess.run(loss,feed_dict = {xs:x_data, ys:y_data}))
        try:
            ax.lines.remove(lines[0])
        except Exception:
            pass
        prediction_value = sess.run(prediction,feed_dict = {xs:x_data})
        lines = ax.plot(x_data,prediction_value,'r-',lw = 5)
        plt.pause(0.1)

#优化器

# conv1   卷积层 1
# pooling1_lrn  池化层 1
# conv2  卷积层 2
# pooling2_lrn 池化层 2
# local3 全连接层 1
# local4 全连接层 2
# softmax 全连接层 3

