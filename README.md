# NS3_auto_tests
### About
Python script to run several NS-3 simulations automatically and parse the result files to extract the required information.

Simulations in NS-3 are run from the command line along with its parameter options:
```{r}
./waf --run "testFile.cc [param1=value1] [param2=value2] ..."
```
This python script assembles the above script for each ns-3 simulation based on the param/values espeficied inside the python script and then executes it on the command line. After the ns-3 simulation finishes, it generates Mesh Point report files and a Flow Monitor report file that are read by python, the required information is extracted and summarized in csv files.

Simulation are especified inside the python script:
1. As a list containing the different strings of param=value pairs for each simulation, or
2. By especifying a dictionary with different values for each param, the python script then will combine all those parameter values and execute all simulations resulting from the combination of those parameter values.

### Options
Especify these options as arguments to the python script.
```{r}
python3 runTests.py combine
```
Used to especify tests as dictionaries with values for each parameter. This is the preferred method when multiple tests are required.
```{r}
python3 runTests.py combine skip=5
```
Used to continue the execution of the batch tests after it was interrupted.
`skip=5`, causes the script to skip the first 5 tests and continue from test #6.
