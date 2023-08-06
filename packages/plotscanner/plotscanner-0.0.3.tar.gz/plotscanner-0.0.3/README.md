# Plotscanner

A __Python3__ application used to convert images of functional data plots to digital format.
Often data is presented in documents or scientific articles in the form of figures. In order to use this data, it must be digitized in some way. This program allows you to get a scanned image of a plot in _JPEG_ or _PNG_ format and quickly digitize the values. The numbers can be saved to a file (_CSV_, _XLS_, _TXT_, etc.) and used.

## Documentation 
You can find the documentation for all of the application's basic modules [here](https://github.com/IlS0/Plot-digitization/tree/main/docs/plotscanner).

## Installation
`$ pip install plotscanner`


### Docker-image

You can download a docker-image of the application if you want to use the back-end part in the container

`$ docker pull ils0/plotscanner`

or build it yourself with the following command:

`$ docker build -t plotscanner .`


## Run
Start the application by running the command in the terminal:
`$ plotscanner`

Follow the instructions in the app window to work correctly.
### Image preparing
Plotscanner requires the input data in the correct form to work right. Before loading the image, crop it and save only the axes and lines of the plot like this.
![Example image](./plotscanner/readme_imgs/example.jpg)
