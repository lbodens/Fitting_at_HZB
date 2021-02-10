import matplotlib as mpl
import yaml, json, lmfit

## json

data_json  = json.load(open("test_param.json"))
parameters = lmfit.Parameters()
for p_name, p_vals in data_json.items():
    parameters.add(lmfit.Parameter(p_name, **p_vals))
print("Created these parameters: ", parameters)


##################################################################
### get new values after fit, think of this as fit_res = model.fit(y, x=x, params=parameters)!
class EmptyObject(object):
    def __init__(self):
        pass
fit_res = EmptyObject() 
setattr(fit_res, "values", {
    "test"          : 0,
    "test2"         : 1,
    "v0_1_amplitude": 30000,
    "v0_1_center"   : 860,
    "v0_1_sigma"    : 0.7,
    "v0_1_gamma"    : 0.0000000001
})
print(fit_res)
##################################################################


updated_values = dict(data_json)
for p_name, p_value in fit_res.values.items():
    # important, otherwise expr will not work anymore!
    if parameters[p_name].vary:
        updated_values[p_name]["value"] = p_value
json.dump(updated_values, open("updated_test_param.json", "w"))


#YAML
data_yaml = yaml.load(open('test_param.yaml'), Loader=yaml.FullLoader)
params = lmfit.Parameters()
for p_name, p_vals in data_yaml.items():
    params.add(lmfit.Parameter(p_name, **p_vals))
print("Created these parameters:", params)

#### do stuff and get fit_res

updated_values = dict(data_yaml)
for p_name, p_value in fit_res.values.items():
    # important, otherwise expr will not work anymore!
    if params[p_name].vary:
        updated_values[p_name]["value"] = p_value
yaml.dump(updated_values, open("updated_test_param.yaml", "w"))
