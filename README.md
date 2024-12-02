# Table of Contents
- [1. Introduction](#1-introduction)
- [2. Getting Started](#2-getting-started)
- [3. Creating Linear Regression Models](#3-creating-linear-regression-models)
	- [3.1 Opening a Dataset](#31-opening-a-dataset)
	- [3.2 Creating a Model](#32-creating-a-model)
	- [3.3 Predicting a Value](#33-predicting-a-value)
- [4. Saving and Loading Models](#4-saving-and-loading-models)
	- [4.1 Saving Models](#41-saving-models)
	- [4.2 Loading Models](#42-loading-models)
- [5. Troubleshooting](#5-troubleshooting)
	- [5.1 I Cannot Open My Dataset](#51-i-cannot-open-my-dataset)
	- [5.2 I Cannot Load My Model](#52-i-cannot-load-my-model)
- [6. Glossary](#6-glossary)

# 1. Introduction
Welcome to the repository for ModelMaker!

This application provides a simple but powerful way to analyze your datasets and visualize linear regression models. By importing a dataset into the application, you can automatically generate a linear regression model; no manual are calculations needed!

This usable, accessible, and lightweight tool is perfect for students, data enthusiasts, and professionals alike.

# 2. Getting Started
Learning how to use ModelMaker's features is key to achieving the results you want. This section explains how to get the most out of the program.

Once you have launched the application, you will need to become familiar with the user interface, as shown in Figure 2.1.

By default, the only visible parts of the interface are the **Open** and **Load** buttons and the path for the file you have opened in the application, though it remains empty until a file is opened.

![The Linear Regression Application window upon startup with no dataset loaded.](https://i.ibb.co/M8YX6ZH/Model-Maker-Default.png)

*Figure 2.1: The appearance of ModelMaker after launching the program*

Immediately upon launch, what is shown in Figure 2.1 is all that will be visible; more of the interface will become visible after you have opened a dataset, as shown in Figure 2.2. After your dataset has been opened, the application window will display the raw data from the dataset.

The raw data is displayed along with two lists. The items in the lists correspond to the columns in your dataset and represent your independent and dependent variables, respectively.

![The Linear Regression Application window with a dataset loaded and displayed.](https://i.ibb.co/23vJgCz/Model-Maker-Dataset.png)

*Figure 2.2: ModelMaker view with a dataset loaded*

After a model has been created, it will be displayed in the application window, as shown in Figure 2.3.

![The Linear Regression Application window with a model loaded and displayed.](https://i.ibb.co/7QYBNcN/Model-Maker-Model.png)

*Figure 2.3: ModelMaker view after a model has been created*

Figure 2.4 shows the equations used to calculate the model, including the predicted equation used to create the model, the R-squared value, and the Mean Square Error value.

![Math equations after generating a model in ModelMaker](https://i.ibb.co/GsXnhmR/Model-Maker-Math.png)

*Figure 2.4: Formulas generated after creating a model in ModelMaker*

You will also find an entry field where you can enter a description for your model and the **Download** button, which is used to save the model you created.

# 3. Creating Linear Regression Models
You must first open a dataset before you can begin using the application to create linear regression models.

## 3.1 Opening a Dataset
Datasets are required for creating a linear regression model; without one, there is no data on which to perform calculations.

**To open a dataset**
1. Select **Open**.

&ensp;&ensp;&ensp;&ensp;The **File Explorer** opens.

2. Navigate to the save location of the dataset you wish to use.

3. Double-click the file.

&ensp;&ensp;&ensp;&ensp;A confirmation window appears that says the data has been read successfully.

4. Select **OK**.

&ensp;&ensp;&ensp;&ensp;The main display shows the dataset.
	
## 3.2 Creating a Model
With your dataset opened in the application, you can begin creating your linear regression models using the module shown in Figure 3.1.

![ModelMaker input columns](https://i.ibb.co/gRyfrnn/Model-Maker-Inputs.png)

*Figure 3.1: The column selection module in ModelMaker*

**To create a linear regression model**
1. Select an item in the **Input Column**.

&ensp;&ensp;&ensp;&ensp;The item you select will become the independent variable in your linear regression model.

2. Select an item in the **Output Column**.

&ensp;&ensp;&ensp;&ensp;The item you select will become the dependent variable in your linear regression model.

3. Select **Confirm selection**.

&ensp;&ensp;&ensp;&ensp;A dialogue box appears, confirming the items you chose.

4. Select **OK**.

&ensp;&ensp;&ensp;&ensp;If your selection is error-free (such as an item with values equal to zero), a dialogue box appears.

5. Select **OK**.

6. Select **Create Linear Regression Model**.

&ensp;&ensp;&ensp;&ensp;A dialogue box appears, indicating the successful creation of a model.

7. Select **OK**.

&ensp;&ensp;&ensp;&ensp;The linear regression model using your independent and dependent variables appears.

## 3.3 Predicting a Value
After you have created your model, you can use the data in your dataset to predict the value of a new number as if it were entered into the dataset.
This can help you make informed decisions using hypothetical data points without the need for manual calculations.

![Value prediction field in ModelMaker](https://i.ibb.co/0FZCF4j/Model-Maker-Maths.png)

*Figure 3.2: Value prediction field in ModelMaker*

**To predict a value**
1. Enter a value in the **PREDICT A VALUE** entry field, shown in Figure 3.2.

&ensp;&ensp;&ensp;&ensp;The value you predict will correspond to the item you chose for the input column.

2. Select **Predict**.

&ensp;&ensp;&ensp;&ensp;The predicted value displays. The value displayed is an estimate of where your entered value would appear along the Y-axis of the model.

# 4. Saving and Loading Models
After you've created your linear regression models, you might want to save them for later use. This can be especially useful if you want to generate multiple models using the same dependent or independent variables with different opposing variables.

## 4.1 Saving Models
Saving a model for later use is easy and can be especially useful if you are working with a large dataset that will require multiple models to be made.

Saving a model is performed with the module shown in Figure 4.1.
![Save module in ModelMaker](https://i.ibb.co/gVhrdB4/Model-Maker-Saving.png)

*Figure 4.1: The save module in ModelMaker*

**To save a model**
1. Enter a description for your model in the entry field.

&ensp;&ensp;&ensp;&ensp;**Note**: Entering a description is optional, but it can be useful for storing information when you return to the model later.

2. Select **Download**.

&ensp;&ensp;&ensp;&ensp;**Note**: If you did not enter a description for your model, a window will appear to indicate this. To close this window, select **OK**.

3. Enter a name for your model.

4. Select a file type for your model.

&ensp;&ensp;&ensp;&ensp;You can choose between the Pickle (.pkl) and Joblib (.jbl) file types when saving.

5. Select **Save**.

&ensp;&ensp;&ensp;&ensp;Your model saves as the chosen file type, and a window will appear.

&ensp;&ensp;&ensp;&ensp;**Note**: By default, the save location is the same location you opened the application from (your downloads folder, for example).

6. Select **OK**.

&ensp;&ensp;&ensp;&ensp;The window closes, confirming that you have saved your model.

## 4.2 Loading Models
After you've saved a model, you might want to load it again in the application later. This can be useful if you need to see the equations produced by the model, such as the R-squared value or the Mean Square Error (MSE).

**To load a model**
1. Select **Load**.

&ensp;&ensp;&ensp;&ensp;A file explorer window appears. By default, it opens to the same location you opened the application from (your downloads

&ensp;&ensp;&ensp;&ensp;folder, for example).

2. Select your saved model.

3. Select **Open**.

&ensp;&ensp;&ensp;&ensp;A window appears, confirming that your model was opened in the application.

4. Select **OK**.

&ensp;&ensp;&ensp;&ensp;Your model appears in the application, as shown in Figure 4.2, along with its description (if you added one when you saved it originally).

![The Linear Regression App window with a model loaded that was previously saved.](https://i.ibb.co/yXKrMMV/Model-Maker-Loaded.png)

*Figure 4.2: A loaded model in ModelMaker*

# 5. Troubleshooting
You might encounter an issue while using the application. While the development team has thoroughly tested it, we cannot account for every error you might encounter. In this section, you will learn how to troubleshoot the two most common issues that may occur while using ModelMaker.

## 5.1 I Cannot Open My Dataset
When trying to open your data set using the application, you might notice that you are either unable to find it using the file explorer.

This is because the application will not allow you to open a dataset that does not use one of the file extensions shown in Table 5.1.

| Compatible Datasets | File Extensions |
|--|--|
| CSV | .csv |
| Excel| .xlsx |
|  | .xls |
| SQL | .db |
|  | .sqlite |

*Table 5.1: Compatible datasets and their file extensions*

## 5.2 I Cannot Load My Model
If you save a model and are unable to load it in ModelMaker, check that the file extension has not changed. If the file extension is incompatible with ModelMaker, you will not be able to find it in the file explorer when you select the option to load a model.

Only the file extensions shown in Table 5.2 are compatible with the application.

| Python Library | File Extension |
|--|--|
| Pickle | .pkl |
| JobLib | .jbl |

*Table 5.2: Compatible file extensions for loading models*

# 6. Glossary
| Terms Used | Definition  |
|--|--|
| Comma-separated Values (CSV) | A file format that stores data in a table-structure. |
| Dataset | A collection of related sets of information used in computer programs. |
| File Explorer | The default file management application on Windows computers.
| GitHub | A platform used by developers to create, share, and collaborate on their code. |
| Linear Regression Model | A mathematical model that estimates the relationship between a dependent and an independent variable.
| Python | A high-level, general-use programming language. |
| Structured Query Language (SQL) | A programming language used to manage data. |

*Table 6.1: Table of terms used and their definitions*
