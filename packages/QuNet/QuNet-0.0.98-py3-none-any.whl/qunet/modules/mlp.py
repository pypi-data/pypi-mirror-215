﻿import math, copy
import torch, torch.nn as nn

from ..utils   import Config
from .total  import get_activation

#========================================================================================

class UnitTensor(nn.Module):
    def forward(self, x):
        return torch.nn.functional.normalize(x, p=2, dim=-1)

#========================================================================================

class MLP(nn.Module):
    def __init__(self,  *args, **kvargs) -> None:
        """
        Fully connected network with one or more hidden layers:
        (B,*, input) -> (B,*, output).

        Args
        ------------
            input (int=None):
                number of inputs > 0
            output (int=None):
                number of outputs > 0
            hidden (int or list = None):
                number of neurons in the hidden layer
            stretch (int = None):            
                if there is, then hidden = int(stretch*input)
            norm (bool = False):
                project a feature vector onto a sphere
            fun (str='gelu'):
                activation function: gelu, relu, sigmoid, tanh, relu6, swish, hswish, hsigmoid
            drop  (float:0.0):
                dropout at the output of the hidden layer

        If there is more than one layer - hidden is a list of the number of neurons in each layer
        There may be no hidden layer: hidden == 0 or == [] or stretch == 0,
        then it's a normal input -> output line layer with no activation function

        Example
        ------------
        ```
            mlp = MLP(input=32, stretch=4, output=1)
            y = mlp( torch.randn(1, 32) )
        ```
        Can be created from config:
        ```
            cfg = MLP.default()
            cfg(input = 3, output = 1)
            mlp = MLP(cfg)
        ```
        And also from the config and key-val arguments:
        ```
            mlp = MLP(cfg, hidden=[128, 512])
        ```
        """
        super().__init__()
        self.cfg = MLP.default()
        self.cfg.set(*args, **kvargs)
        self.create()

    #---------------------------------------------------------------------------

    @staticmethod
    def default():
        return copy.deepcopy(Config(
            input   = None,     # number of inputs > 0
            output  = None,     # number of outputs > 0
            hidden  = None,     # number of neurons in the hidden layer (int or list)
            stretch = None,     # if hiddem is None, then hidden = int(stretch*input)
            norm    = False,    # 
            fun     = 'gelu',   # activation function: gelu, relu, sigmoid, tanh
            drop    =  0,       # dropout at the output of the hidden layer
        ))

    #---------------------------------------------------------------------------

    def forward(self, x):
        x = self.layers(x)
        return x

    #---------------------------------------------------------------------------

    def prepare(self):
        cfg=self.cfg
        assert cfg.input is not None  and cfg.output is not None,  f'MLP: wrong input/output: {cfg.get_str()}'

        if type(cfg.hidden) is list:
            self.neurons = [cfg.input] + cfg.hidden + [cfg.output]
        else:
            if (cfg.hidden is None) and (cfg.stretch is not None):
                cfg.hidden = int(cfg.stretch * cfg.input)

            if cfg.hidden is None or cfg.hidden <= 0:
                self.neurons = [cfg.input, cfg.output]
            else:
                self.neurons = [cfg.input, cfg.hidden, cfg.output]

        if cfg.fun not in ['gelu', 'relu', 'sigmoid', 'tanh', 'relu6', 'swish', 'hswish', 'hsigmoid']:
            print(f"MLP warning: unknown activation function {cfg.fun}, set to gelu")
            cfg.fun  = 'gelu'

    #---------------------------------------------------------------------------

    def create(self):
        self.prepare()
        seq = []
        for i in range (1, len(self.neurons)):
            seq += [ nn.Linear(self.neurons[i-1],  self.neurons[i]) ]
            if i+1 < len(self.neurons):
                seq += [get_activation(self.cfg.fun),
                        nn.Dropout(self.cfg.drop)     ]
                if self.cfg.norm:
                    seq += [ UnitTensor() ]
        self.layers = nn.Sequential(*seq)

    #---------------------------------------------------------------------------

    @staticmethod
    def unit_test():
        mlp = MLP(input=32, stretch=4, output=1)
        y = mlp( torch.randn(1, 32) )

        cfg = MLP.default()
        cfg(input = 3, output = 1)
        mlp = MLP(cfg)

        mlp = MLP(cfg, hidden=[128, 512])

        mlp = MLP(cfg, hidden=128, norm=True)

        print("ok MLP")
        return True

#========================================================================================    

class SkipMLP(nn.Module):
    def __init__(self,  *args, **kvargs) -> None:
        """
        Args
        ------------
            n_blocks (int=2):
                number of transformer blocks
            mlp ( Config=MLP.default() ):
                should be: input == output

        Example
        ------------
        ```
            mlp = SkipMLP(n_blocks=5, mlp=Config(input=32, hidden=[128,128], output=32))
            y = mlp( torch.randn(1, 32) )
        ```
        """
        super().__init__()
        self.cfg = SkipMLP.default()
        cfg = self.cfg.set(*args, **kvargs)
        
        assert cfg.mlp.input == cfg.mlp.output, f"In mlp should be input ({cfg.mlp.input}) == output ({cfg.mlp.output})"

        self.blocks = nn.ModuleList([  MLP(cfg.mlp)                 for _ in range(cfg.n_blocks) ])
        self.norms  = nn.ModuleList([  nn.LayerNorm (cfg.mlp.input) for _ in range(cfg.n_blocks) ] )

    #---------------------------------------------------------------------------

    @staticmethod
    def default():
        return copy.deepcopy(Config(
            n_blocks = 1,
            mlp = MLP.default(), 
        ))

    #---------------------------------------------------------------------------

    def forward(self, x):
        for block, norm in zip(self.blocks, self.norms):            
            x = block(norm(x)) + x                        
        return x
    
    #---------------------------------------------------------------------------

    @staticmethod
    def unit_test():
        mlp = SkipMLP(n_blocks=5, mlp=Config(input=32, hidden=[128,128], output=32))
        y = mlp( torch.randn(1, 32) )
        print(f"ok SkipMLP: {y.shape}")
        return True

#========================================================================================

