# Importing required packages
import pandas as pd
from neuralprophet import NeuralProphet #NeuralProphet is a library for time series forecasting that utilizes neural networks.
from sklearn.metrics import mean_absolute_percentage_error
from greykite.framework.templates.autogen.forecast_config import ForecastConfig
from greykite.framework.templates.forecaster import Forecaster
from greykite.framework.templates.model_templates import ModelTemplateEnum
from greykite.framework.templates.autogen.forecast_config import ModelComponentsParam

# Function to train silverkite model
#This line defines a Python function called train_greykite that takes three arguments:
#data: A pandas DataFrame containing the time series data.
#metadata: Metadata information used in the Greykite forecasting configuration.
#regressor_col: A list of regressor columns used in the forecasting model.
def train_greykite(data, metadata, regressor_col):
    forecaster = Forecaster() #to configure and train a forecasting model based on the Greykite framework.
    #specifying model components, growth terms, changepoints, and other forecasting parameters.
    result = forecaster.run_forecast_config(
        df=data.reset_index(),
        config=ForecastConfig(
            model_template=ModelTemplateEnum.SILVERKITE.name,
            forecast_horizon=20,  # forecasts 20 steps ahead
            coverage=0.95,  # 95% prediction intervals
            metadata_param=metadata,
            model_components_param=ModelComponentsParam(
                autoregression=None,
                regressors=regressor_col,
                events={
                    "holidays_to_model_separately": "auto",
                    "holiday_lookup_countries": ["UnitedStates"]
                },
                growth={
                    "growth_term": "linear"
                },
                changepoints={
                    "changepoints_dict": dict(
                        method="auto",
                        yearly_seasonality_order=10,
                        regularization_strength=0.5,
                        potential_changepoint_n=5,
                        yearly_seasonality_change_freq="365D",
                        no_changepoint_distance_from_end="365D"
                    )
                }
            )
        )
    )
    # Making evaluation dataframe and printing it
    #The evaluation metrics for the fitted Silverkite model are computed and stored in evaluation_grekite_df, which is then printed.
    evaluation_grekite_df= pd.DataFrame(result.forecast.compute_evaluation_metrics_split())
    print("evaluation matrix for fitted silverkite model \n ",evaluation_grekite_df)
    return result

# Function to train Neural Prophet model
def train_neural_prophet(data, future_reg):
    test_length = 20
    df_train = data.iloc[:-test_length]
    df_test = data.iloc[-test_length:]
    #An instance of the NeuralProphet model is created with specific configuration settings such as loss function, number of changepoints, and seasonality mode.
    model = NeuralProphet(loss_func='MSE', n_changepoints=2, seasonality_mode='additive')
    #Future regressors are added to the model using the add_future_regressor method.
    for col in future_reg:
        model.add_future_regressor(col)#The model is fitted to the training data.
    metrics = model.fit(df_train, freq="W")
    future_df = model.make_future_dataframe(df_test, periods=test_length, n_historic_predictions=len(df_test),
                                            regressors_df=df_test)
    #The model is used to make predictions on the test data, and the mean absolute percentage error is computed and printed.
    forecast = model.predict(future_df)
    print(f"Mean absolute percentage error for fitted NeuralProphet model is \t{mean_absolute_percentage_error(df_test['y'], forecast.iloc[-test_length:]['yhat1']):.4f}")
    return model

