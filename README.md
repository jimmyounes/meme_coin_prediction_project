# meme_coin_prediction_project
This project focuses on developing a personal initiative aimed at scraping new cryptocurrency pairs from DexScreeners and forecasting the growth of meme coins. Leveraging historical data from existing meme coins, the goal is to construct a time series model for training and predicting future pairs in the market.


First step : 

I collected data from Dexscreener over a span of five days. After preprocessing the data, I applied an LSTM model, but the resulting score was only 0.71. This lower score indicates that the model might not have had enough representative data or features to make accurate predictions.

To enhance the performance of my script, I plan to augment the feature set by incorporating additional data points. For instance, I intend to retrieve information such as the number of token holders and a Twitter score. The number of holders can provide insights into the token's popularity and distribution, while the Twitter score can capture sentiments or discussions regarding the token on Twitter. By including these additional features, I aim to enrich the dataset and improve the model's ability to capture relevant patterns and trends, ultimately leading to more accurate predictions.


Second step : 

In the second step, the script will retrieve live data and make predictions on coins that have passed their first phase of creation. If the model predict 1 , typically if it's predicted to perform well, the script will send an email notification to subscribers.
