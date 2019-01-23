import tensorflow as tf
import numpy as np

#creat data
x_data = np.random.rand(100).astype(np.float32)
y_data = x_data * 0.1 + 0.3


###creat tensfloat structure state###
Weights = tf.Variable(tf.random_uniform([1],-1.0,1.0))
biases = tf.Variable(tf.zeros([1]))

y = Weights*0.1 + biases

loss = tf.reduce_mean(tf.square(y - y_data))
optimizer = tf.trian.GradientDescentOptimizer(0.5)#优化器
trian = optimizer.minimize()#优化损失函数，减少误差，每步都要做

init = tf.initialize_all_variables()
###creat tensfloat structure state###

sess = tf.Session()
sess.run(init)

for step in range(201):
    sess.run(trian)
    if step % 20==0:
        print(step,sess.run(Weights),sess.run(biases))