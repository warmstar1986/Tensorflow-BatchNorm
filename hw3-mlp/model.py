# -*- coding: utf-8 -*-

import tensorflow as tf


class Model:
    def __init__(self,
                 is_train,
                 learning_rate=0.001,
                 learning_rate_decay_factor=0.9995):
        self.x_ = tf.placeholder(tf.float32, [None, 28*28])
        self.y_ = tf.placeholder(tf.int32, [None])
        self.keep_prob = tf.placeholder(tf.float32)
        # tf.reset_default_graph()
        # TODO:  implement input -- Linear -- BN -- ReLU -- Linear -- loss
        #        the 10-class prediction output is named as "logits"
        rows, columns = map(lambda i: i.value, self.x_.get_shape())
        print(rows,columns)
        print(self.x_.shape)
        l1 = add_layer(self.x_,784,392,tf.nn.relu)
        # l2 = add_layer(l1,392,200,tf.nn.relu)
        # l3 = add_layer(l2,200,100,tf.nn.relu)
        # print(l1.get_shape())
        # axis = list(range(len(l1.get_shape()) - 1))
        # print(axis)
        # self.mean, self.variance = tf.nn.moments(l1,1)
        
        # mean.eval()
        # variance.eval()
        logits = add_layer(l1,392,10,None)
        # print(logits.get_shape())
        # exit(0)

        # logits = tf.Variable(tf.constant(0.0, shape=[100, 10]))  # deleted this line after you implement above layers

        self.loss = tf.reduce_mean(tf.nn.sparse_softmax_cross_entropy_with_logits(labels=self.y_, logits=logits))
        self.correct_pred = tf.equal(tf.cast(tf.argmax(logits, 1), tf.int32), self.y_)
        self.pred = tf.argmax(logits, 1)  # Calculate the prediction result
        self.acc = tf.reduce_mean(tf.cast(self.correct_pred, tf.float32))  # Calculate the accuracy in this mini-batch

        self.learning_rate = tf.Variable(float(learning_rate), trainable=False, dtype=tf.float32)
        self.learning_rate_decay_op = self.learning_rate.assign(self.learning_rate * learning_rate_decay_factor)  # Learning rate decay

        self.global_step = tf.Variable(0, trainable=False)
        self.params = tf.trainable_variables()
        self.train_op = tf.train.AdamOptimizer(self.learning_rate).minimize(self.loss, global_step=self.global_step,
                                                                            var_list=self.params)  # Use Adam Optimizer

        self.saver = tf.train.Saver(tf.global_variables(), write_version=tf.train.SaverDef.V2,
                                    max_to_keep=3, pad_step_number=True, keep_checkpoint_every_n_hours=1.0)


def add_layer(inp,in_size,out_size,active_function):
    Weight = weight_variable([in_size,out_size])
    bias = bias_variable([out_size])


    Wx_plus_b = tf.matmul(inp,Weight) + bias
    Wx_plus_b = batch_normalization_layer(Wx_plus_b)
    if active_function is None:
        output = Wx_plus_b
    else:
        output = active_function(Wx_plus_b)
    return output

def weight_variable(shape):  # you can use this func to build new variables
    initial = tf.truncated_normal(shape, stddev=0.1)
    return tf.Variable(initial)


def bias_variable(shape):  # you can use this func to build new variables
    initial = tf.constant(0.1, shape=shape)
    return tf.Variable(initial)


def batch_normalization_layer(inputs, isTrain=False):
    # TODO: implemented the batch normalization func and applied it on fully-connected layers
    
    in_size, out_size = inputs.get_shape()
    mean, var = tf.nn.moments(inputs,[0])
    scale = tf.Variable(tf.ones([out_size]))
    shift = tf.Variable(tf.ones([out_size]))
    eps = 0.001
    if isTrain:
        inputs = tf.nn.batch_normalization(inputs,mean,var,shift,scale,eps)
    else:
        print('fuck')
    return inputs


