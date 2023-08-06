<p align="center">
        <a>
	    <img src='https://img.shields.io/badge/python-3.7%7C3.8%7C3.9%2B-blueviolet' alt='Python' />
	</a>
	<a href='https://XGen.readthedocs.io/en/latest/?badge=latest'>
    	    <img src='https://readthedocs.org/projects/XGen/badge/?version=latest' alt='Documentation Status' />
	</a>
	<a href='https://creativecommons.org/licenses/by/4.0/'>
	    <img alt="CC 4.0 - License" src="https://img.shields.io/badge/License-CC_BY_4.0-lightgrey.svg">
	</a><br>
</p>

</p>
<p align="center">
 <a>
  <img src="doc/source/_static/logo.png"  width="300" height="100">
 </a><br>
  <a href="https://XGen.readthedocs.io/en/latest/"> ➡ Documentation </a>
</p>


    
This library offers a comprehensive implementation of various generative models, all unified under a single framework. It enables benchmark experiments and facilitates model comparisons by training the models using the same autoencoding neural network architecture. With the "make your own generative time series" feature, you can train any of these models using your own data and customize the Encoder and Decoder neural networks as per your requirements.

Additionally, the library integrates popular experiment monitoring tools such as [wandb](https://wandb.ai/), [mlflow](https://mlflow.org/), and [comet-ml](https://www.comet.com/signup?utm_source=XGen&utm_medium=partner&utm_campaign=AMS_US_EN_SNUP_XGen_Comet_Integration) 🧪. It also allows for easy model sharing and loading from the [HuggingFace Hub](https://huggingface.co/models) 🤗 with just a few lines of code.

![An overview of XGen framework interacted with XGen Archive](doc/source/_static/overview_xgen.png)

<object data="doc/source/_static/overview_xgen.pdf" type="application/pdf" width="700px" height="400px">
    <embed src="doc/source/_static/overview_xgen.pdf">
        <p>This browser does not support PDFs. Please download the PDF to view it: <a href="doc/source/_static/overview_xgen.pdf">Download PDF</a>.</p>
    </embed>
</object>

**Note**
> Your ```XGen Time Series``` now supports distributed training using PyTorch's DDP (Distributed Data Parallel). With this new feature, you can now train your preferred Generative Time Series models faster and on custom datasets, all with just a few lines of code. This allows for improved scalability and accelerated training across multiple GPUs or even distributed systems.
> To showcase the enhanced performance, we have conducted a comprehensive benchmarking analysis. You can find the detailed results in the benchmark section of our documentation. This benchmark highlights the significant speed-up achieved by leveraging the distributed training capabilities of XGen Time Series.
> Take advantage of XGen 0.2's distributed training support and experience accelerated training for your Generative Time Series models. Visit our documentation and explore the benchmark section to learn more about the performance improvements and how to make the most out of this latest release.


## Quick access:
- [Installation](#installation)
- [Implemented models](#available-models) / [Implemented samplers](#available-samplers)
- [Reproducibility statement](#reproducibility) / [Results flavor](#results)
- [Model training](#launching-a-model-training) / [Data generation](#launching-data-generation) / [Custom network architectures](#define-you-own-autoencoder-architecture) / [Distributed training](#distributed-training-with-XGen)
- [Model sharing with 🤗 Hub](#sharing-your-models-with-the-huggingface-hub-) / [Experiment tracking with `wandb`](#monitoring-your-experiments-with-wandb-) / [Experiment tracking with `mlflow`](#monitoring-your-experiments-with-mlflow-) / [Experiment tracking with `comet_ml`](#monitoring-your-experiments-with-comet_ml-)
- [Tutorials](#getting-your-hands-on-the-code) / [Documentation](https://XGen.readthedocs.io/en/latest/)
- [Contributing 🚀](#contributing-) / [Issues 🛠️](#dealing-with-issues-%EF%B8%8F)
- [Citing this repository](#citation)

# Installation

To install the latest stable release of this library run the following using ``pip``

```bash
$ pip install XGen
``` 

To install the latest github version of this library run the following using ``pip``

```bash
$ pip install git+https://github.com/XgenTimeSeries/xgen-timeseries
``` 

or alternatively you can clone the github repo to access to tests, tutorials and scripts.
```bash
$ git clone https://github.com/XgenTimeSeries/xgen-timeseries
```
and install the library
```bash
$ cd xgen-timeseries
$ pip install -e .
``` 

## Available Models

Below is the list of the models currently implemented in the library.


|               Models               |                                                                                    Training example                                                                                    |                     Paper                    |                           Official Implementation                          |
|:----------------------------------:|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------:|:--------------------------------------------:|:--------------------------------------------------------------------------:|
| PSA-GAN                   | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](#) |                    [link](https://arxiv.org/abs/2108.00981)                             |  
| WaveGAN                   | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](#) |                    [link](https://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=9053795)                             |                                                                         |
| TimeGAN                   | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](#) |                    [link](https://arxiv.org/pdf/1706.02633.pdf)                             |                                                                         |
| GT-GAN                   | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](#) |                      [link](https://arxiv.org/pdf/1706.02633.pdf)                           |                                                                         |
| RCGAN                   | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](#) |                      [link](https://arxiv.org/pdf/1706.02633.pdf)                           |                                                                         |
| Professor Forcing                   | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](#) |                       [link](https://arxiv.org/pdf/1706.02633.pdf)                          |                                                                         |
| RGAN                   | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](#) |                    [link](https://arxiv.org/pdf/1706.02633.pdf)                             |                                                                      |



**See [reconstruction](#Reconstruction) and [generation](#Generation) results for all models**

## Reproducibility

We validate the implementations by reproducing some results presented in the original publications when the official code has been released or when enough details about the experimental section of the papers were available. 

## Training Step

To launch a model training, you only need to call a `TrainingPipeline` instance. 

```python
       from XGen.pipelines import TrainingPipeline
       from XGen.models import VAE, VAEConfig
       from XGen.trainers import BaseTrainerConfig

       # Set up the training configuration
       my_training_config = BaseTrainerConfig(
   	output_dir='my_model',
   	num_epochs=50,
   	learning_rate=1e-3,
   	per_device_train_batch_size=200,
   	per_device_eval_batch_size=200,
   	train_dataloader_num_workers=2,
   	eval_dataloader_num_workers=2,
   	steps_saving=20,
   	optimizer_cls="AdamW",
   	optimizer_params={"weight_decay": 0.05, "betas": (0.91, 0.995)},
   	scheduler_cls="ReduceLROnPlateau",
   	scheduler_params={"patience": 5, "factor": 0.5}
    )
       # Set up the model configuration 
       my_xgen_config = XGenConfig(
   	input_dim=(28, 3600), # (features_time, time_sequence_szie)
   	latent_dim=10
    )
       # Build the model
       my_xgen_model = XGenModel(
   	model_config=my_xgen_config
    )
       # Build the Pipeline
       pipeline = TrainingPipeline(
    	training_config=my_training_config,
    	model=my_vae_model
    )
       # Launch the Pipeline
       pipeline(
   	train_data=your_train_data, # must be torch.Tensor, np.array or torch datasets
   	eval_data=your_eval_data # must be torch.Tensor, np.array or torch datasets
    )
```

At the end of training, the best model weights, model configuration and training configuration are stored in a `final_model` folder available in  `my_model/MODEL_NAME_training_YYYY-MM-DD_hh-mm-ss` (with `my_model` being the `output_dir` argument of the `BaseTrainerConfig`). If you further set the `steps_saving` argument to a certain value, folders named `checkpoint_epoch_k` containing the best model weights, optimizer, scheduler, configuration and training configuration at epoch *k* will also appear in `my_model/MODEL_NAME_training_YYYY-MM-DD_hh-mm-ss`.

##  Training on XGen Time Series datasets
We also provide a training script example [here](https://github.com/XgenTimeSeries/xgen-timeseries/tree/main/examples/scripts/training.py) that can be used to train the models on benchmarks datasets (Ukdale, Refit, Redd    ).

```bash
python training.py --dataset ukdale --model_name TimeGAN --model_config 'configs/ae_config.json' --training_config 'configs/base_training_config.json'
```

See [README.md](https://github.com/XgenTimeSeries/xgen-timeseries/tree/main/examples/scripts/README.md) for further details on this script

## Generate new Time Series

### Using the `GenerationPipeline`

The easiest way to launch a data generation from a trained model consists in using the built-in `GenerationPipeline` provided in XGen. Say you want to generate 100 samples using a `MAFSampler` all you have to do is 1) relaod the trained model, 2) define the sampler's configuration and 3) create and launch the `GenerationPipeline`.


### Samplers Modules

You can launch the data generation process from a trained model directly with the sampler. For instance, to generate new data with your sampler, run the following.

```python
       from XGen.models import AutoModel
       from XGen.samplers import NormalSampler
       # Retrieve the trained model
       my_trained_vae = AutoModel.load_from_folder(
   	'path/to/your/trained/model'
    )
       # Define your sampler
       my_samper = NormalSampler(
   	model=my_trained_xgen
    )
       # Generate samples
       gen_data = my_samper.sample(
   	num_samples=50,
   	batch_size=10,
   	output_dir=None,
   	return_gen=True
    )
```
If you set `output_dir` to a specific path, the generated time series will be saved as `.csv`.


## Your own Model architecture for forecasting or Energy Dissagregation 
 
XGen provides you the possibility to define your own neural networks within the VAE models. For instance, say you want to train a Wassertstein AE with a specific encoder and decoder, you can do the following:

```python
       from XGen.models.nn import BaseEncoder, BaseDecoder
       from XGen.models.base.base_utils import ModelOutput
       class My_Encoder(BaseEncoder):
   	def __init__(self, args=None): # Args is a ModelConfig instance
   		BaseEncoder.__init__(self)
   		self.layers = my_nn_layers()
   		
   	def forward(self, x:torch.Tensor) -> ModelOutput:
   		out = self.layers(x)
   		output = ModelOutput(
   			embedding=out # Set the output from the encoder in a ModelOutput instance 
   		)
   		return output
   
    class My_Decoder(BaseDecoder):
   	def __init__(self, args=None):
   		BaseDecoder.__init__(self)
   		self.layers = my_nn_layers()
   		
   	def forward(self, x:torch.Tensor) -> ModelOutput:
   		out = self.layers(x)
   		output = ModelOutput(
   			reconstruction=out # Set the output from the decoder in a ModelOutput instance
   		)
   		return output
   
       my_encoder = My_Encoder()
       my_decoder = My_Decoder()
```

And now build the model

```python
       from XGen.models import WAE_MMD, WAE_MMD_Config
       # Set up the model configuration 
       my_wae_config = model_config = WAE_MMD_Config(
   	input_dim=(1, 28, 28),
   	latent_dim=10
    )
   
       # Build the model
       my_wae_model = WAE_MMD(
   	model_config=my_wae_config,
   	encoder=my_encoder, # pass your encoder as argument when building the model
   	decoder=my_decoder # pass your decoder as argument when building the model
    )
```

**important note 1**: For all AE-based models (AE, WAE, RAE_L2, RAE_GP), both the encoder and decoder must return a `ModelOutput` instance. For the encoder, the `ModelOutput` instance must contain the embbeddings under the key `embedding`. For the decoder, the `ModelOutput` instance must contain the reconstructions under the key `reconstruction`.


**important note 2**: For all VAE-based models (VAE, BetaVAE, IWAE, HVAE, VAMP, RHVAE), both the encoder and decoder must return a `ModelOutput` instance. For the encoder, the `ModelOutput` instance must contain the embbeddings and **log**-covariance matrices (of shape batch_size x latent_space_dim) respectively under the key `embedding` and `log_covariance` key. For the decoder, the `ModelOutput` instance must contain the reconstructions under the key `reconstruction`.


## Using benchmark neural nets
You can also find predefined neural network architectures for the most common data sets (*i.e.* MNIST, CIFAR, CELEBA    ) that can be loaded as follows

```python
       from XGen.models.nn.benchmark.mnist import (
   	Encoder_Conv_AE_MNIST, # For AE based model (only return embeddings)
   	Encoder_Conv_VAE_MNIST, # For VAE based model (return embeddings and log_covariances)
   	Decoder_Conv_AE_MNIST
    )
```
Replace *mnist* by cifar or celeba to access to other neural nets.

## Distributed Training with `XGen`
As of `v0.1.0`, XGen now supports distributed training using PyTorch's [DDP](https://pytorch.org/doc/stable/notes/ddp.html). It allows you to train your favorite VAE faster and on larger dataset using multi-gpu and/or multi-node training.

To do so, you can build a python script that will then be launched by a launcher (such as `srun` on a cluster). The only thing that is needed in the script is to specify some elements relative to the distributed environment (such as the number of nodes/gpus) directly in the training configuration as follows

```python
       training_config = BaseTrainerConfig(
        num_epochs=10,
        learning_rate=1e-3,
        per_device_train_batch_size=64,
        per_device_eval_batch_size=64,
        train_dataloader_num_workers=8,
        eval_dataloader_num_workers=8,
        dist_backend="nccl", # distributed backend
        world_size=8 # number of gpus to use (n_nodes x n_gpus_per_node),
        rank=5 # process/gpu id,
        local_rank=1 # node id,
        master_addr="localhost" # master address,
        master_port="12345" # master port,
    )
```

See this [example script](https://github.com/XgenTimeSeries/xgen-timeseries/blob/main/examples/scripts/distributed_training_imagenet.py) that defines a multi-gpu VQVAE training on ImageNet dataset. Please note that the way the distributed environnement variables (`world_size`, `rank`    ) are recovered may be specific to the cluster and launcher you use. 

### Benchmark

Below are indicated the training times for a Vector Quantized VAE (VQ-VAE) with `XGen` for 100 epochs on MNIST on V100 16GB GPU(s), for 50 epochs on [FFHQ](https://github.com/NVlabs/ffhq-dataset) (1024x1024 images) and for 20 epochs on [ImageNet-1k](https://huggingface.co/datasets/imagenet-1k) on V100 32GB GPU(s).

|  | Train Data | 1 GPU | 4 GPUs | 2x4 GPUs |
|:---:|:---:|:---:|:---:|---|
| UK DALE | Energy data from UK households | 7h 30min | 3h 12min | 1h 58min |
| REDD | Energy data from US households | 9h 14min | 4h 26min | 2h 53min |
| REFIT | Energy data from UK households | 6h 51min | 3h 02min | 1h 47min |


For each dataset, we provide the benchmarking scripts [here](https://github.com/XgenTimeSeries/xgen-timeseries/tree/main/examples/scripts)


## Sharing your models with the HuggingFace Hub 🤗
XGen also allows you to share your models on the [HuggingFace Hub](https://huggingface.co/models). To do so you need:
- a valid HuggingFace account
- the package `huggingface_hub` installed in your virtual env. If not you can install it with 
```
$ python -m pip install huggingface_hub
```
- to be logged in to your HuggingFace account using
```
$ huggingface-cli login
```

### Uploading a model to the Hub
Any XGen model can be easily uploaded using the method `push_to_hf_hub`
```python
       my_vae_model.push_to_hf_hub(hf_hub_path="your_hf_username/your_hf_hub_repo")
```
**Note:** If `your_hf_hub_repo` already exists and is not empty, files will be overridden. In case, 
the repo `your_hf_hub_repo` does not exist, a folder having the same name will be created.

### Downloading models from the Hub
Equivalently, you can download or reload any XGen's model directly from the Hub using the method `load_from_hf_hub`
```python
       from XGen.models import AutoModel
       my_downloaded_vae = AutoModel.load_from_hf_hub(hf_hub_path="path_to_hf_repo")
```

## Monitoring your experiments with `wandb` 🧪
XGen also integrates the experiment tracking tool [wandb](https://wandb.ai/) allowing users to store their configs, monitor their trainings and compare runs through a graphic interface. To be able use this feature you will need:
- a valid wandb account
- the package `wandb` installed in your virtual env. If not you can install it with 
```
$ pip install wandb
```
- to be logged in to your wandb account using
```
$ wandb login
```

### Use `WandbCallback` for logs
Launching an experiment with time-real logs with `wandb` in XGen Time Series is pretty simple. The only thing a user needs to do is create a `WandbCallback` instance: 

```python
	# Create your callback
	from XGen.trainers.training_callbacks import WandbCallback
	callbacks = [] # the TrainingPipeline expects a list of callbacks
	wandb_callback = WandbCallback() # Build the callback
	wandb_callback.setup(
	training_config=your_training_config, # training config
	model_config=your_model_config, # model config
	project_name="wandb_project", # your and project
	entity_name="wandb_entity", # your wandb entity
    )
       callbacks.append(wandb_callback) # Add it to the callbacks list
```

```python
       pipeline = TrainingPipeline(
   	training_config=config,
   	model=model
    )
       pipeline(
   	train_data=train_dataset,
   	eval_data=eval_dataset,
   	callbacks=callbacks 
    )
       # You can log to https://wandb.ai/your_wandb_entity/your_wandb_project to monitor your training
```
See the detailed tutorial 

## Monitoring your experiments with `mlflow` 🧪
XGen also integrates the experiment tracking tool [mlflow](https://mlflow.org/) allowing users to store their configs, monitor their trainings and compare runs through a graphic interface. To be able use this feature you will need:
- the package `mlfow` installed in your virtual env. If not you can install it with 
```
$ pip install mlflow
```

### Creating a `MLFlowCallback`
Launching an experiment monitoring with `mlfow` in XGen is pretty simple. The only thing a user needs to do is create a `MLFlowCallback` instance   

```python
       # Create you callback
       from XGen.trainers.training_callbacks import MLFlowCallback
       callbacks = [] # the TrainingPipeline expects a list of callbacks
       mlflow_cb = MLFlowCallback() # Build the callback 
       # SetUp the callback 
       mlflow_cb.setup(
   	training_config=your_training_config, # training config
   	model_config=your_model_config, # model config
   	run_name="mlflow_cb_example", # specify your mlflow run
    )
       callbacks.append(mlflow_cb) # Add it to the callbacks list
```
   and then pass it to the `TrainingPipeline`.
```python
       pipeline = TrainingPipeline(
   	training_config=config,
   	model=model
    )
       pipeline(
   	train_data=train_dataset,
   	eval_data=eval_dataset,
   	callbacks=callbacks # pass the callbacks to the TrainingPipeline and you are done!
    )
```
you can visualize your metric by running the following in the directory where the `./mlruns`
```bash
$ mlflow ui 
```
See the detailed tutorial 

## Monitoring your experiments with `comet_ml` 🧪
XGen also integrates the experiment tracking tool [comet_ml](https://www.comet.com/signup?utm_source=XGen&utm_medium=partner&utm_campaign=AMS_US_EN_SNUP_XGen_Comet_Integration) allowing users to store their configs, monitor their trainings and compare runs through a graphic interface. To be able use this feature you will need:
- the package `comet_ml` installed in your virtual env. If not you can install it with 
```
$ pip install comet_ml
```

### Creating a `CometCallback`
Launching an experiment monitoring with `comet_ml` in XGen is pretty simple. The only thing a user needs to do is create a `CometCallback` instance   

```python
       # Create you callback
       from XGen.trainers.training_callbacks import CometCallback
       callbacks = [] # the TrainingPipeline expects a list of callbacks
       comet_cb = CometCallback() # Build the callback 
       # SetUp the callback 
       comet_cb.setup(
   	training_config=training_config, # training config
   	model_config=model_config, # model config
   	api_key="your_comet_api_key", # specify your comet api-key
   	project_name="your_comet_project", # specify your wandb project
   	#offline_run=True, # run in offline mode
   	#offline_directory='my_offline_runs' # set the directory to store the offline runs
    )
       callbacks.append(comet_cb) # Add it to the callbacks list
```
   and then pass it to the `TrainingPipeline`.
```python
       pipeline = TrainingPipeline(
   	training_config=config,
   	model=model
    )
       pipeline(
   	train_data=train_dataset,
   	eval_data=eval_dataset,
   	callbacks=callbacks # pass the callbacks to the TrainingPipeline and you are done!
    )
       # You can log to https://comet.com/your_comet_username/your_comet_project to monitor your training
```
See the detailed tutorial 

## Generation data (Uk-DALE Dataset) 

![An overview of XGen framework interacted with XGen Archive](doc/source/_static/Uk-DALE.png)

## Dealing with issues 🛠️

If you are experiencing any issues while running the code or request new features/models to be implemented please [open an issue on github](https://github.com/XgenTimeSeries/xgen-timeseries/issues).

## Contributing 🚀

You want to contribute to this library by adding a model, a sampler or simply fix a bug ? That's awesome! Thank you! Please see [CONTRIBUTING.md](https://github.com/XgenTimeSeries/xgen-timeseries/tree/main/CONTRIBUTING.md) to follow the main contributing guidelines.

# Citation

If you find this work useful or use it in your research, please consider citing us

```bibtex
@inproceedings{KoublalXGenTS,
 author = {khalid Oublal, Ladjal, Benhaiem, le-borgne and Roueff},
 booktitle = {Advances in Neural Information Processing Systems},
 pages = {21575--21589},
 publisher = {Curran Associates, Inc.},
 title = {XGen: A Comprehensive Archive and an eXplainable Time Series Generation Framework for Energy},
 volume = {35},
 year = {2023}
}
```
