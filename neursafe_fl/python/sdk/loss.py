#  Copyright 2022 The Neursafe FL Authors. All Rights Reserved.
#  SPDX-License-Identifier: Apache-2.0

# pylint:disable=invalid-name,too-many-arguments
"""Loss for client sdk.
"""
import os
from neursafe_fl.python.sdk.utils import get_runtime, TASK_LOSS

FEDDC = "feddc"


def feddc_loss(model, origin_loss_func, sample_num, batch_size, lr, epoch,
               alpha=0.01, **kwargs):
    """
    The feddc loss, used for data heterogeneity in federated learning.
    the loss have 3 components: the local empirical loss term, the penalized
    term, and a gradient correction term. More detail see:
    https://arxiv.org/abs/2203.11751

    Args:
        model: The model will be using to train. and it already loaded
               init weights from server.
        origin_loss_func: Base loss function used for train, such as
                          CrossEntropyLoss in pytorch, the same as
                          categorical_crossentropy in tensorflow.
        sample_num: The number of samples used in this round when training
                    the local model.
        batch_size: The batch size used when training the local model.
        lr: Local training learning rate.
        epoch: The epoch used when training the local model.
        alpha: The hyper-parameter that controls the weight of R, The
               recommended setting value is 0.1/0.01/0.005.
        kwargs:
            device: Use cpu or gpu when run training, only used in pytorch.
            print_loss: Printing detail loss per forward or per call.
    """
    module_name = "neursafe_fl.python.libs.loss.%s.%s" % (
        get_runtime().lower(), FEDDC)
    module = __import__(module_name, fromlist=True)
    class_name = "FeddcLoss"
    return getattr(module, class_name).get_instance(
        model, origin_loss_func=origin_loss_func, sample_num=sample_num,
        batch_size=batch_size, lr=lr,
        epoch=epoch, alpha=alpha, **kwargs)


def get_loss_instance():
    """Get loss instance if already created by *_loss.
    """
    loss_map = {
        FEDDC: "FeddcLoss"
    }

    loss_name = os.getenv(TASK_LOSS)
    module_name = "neursafe_fl.python.libs.loss.%s.%s" % (
        get_runtime().lower(), loss_name)
    module = __import__(module_name, fromlist=True)
    class_name = loss_map[loss_name]
    return getattr(module, class_name).get_instance()
