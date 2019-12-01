# AlphaGomoku

AlphaGomoku is a Gomoku AI based on [Alpha Zero's algorithm](https://deepmind.com/blog/alphago-zero-learning-scratch/).

**Chinese:** AlphaGomoku 是個基於[Alpha Zero 演算法](https://deepmind.com/blog/alphago-zero-learning-scratch/)演算法的五子棋AI。 本專案需要安裝[Keras](https://keras.io/)

# How to run
After cloning the project, training can be started by running **model_training/agc_training.py**. 
Testing of trained models can be done in **playground.py**.

Please note that the training may take while, because it requires at least a 4000+ games to achieve reasonable results. It is also recommended to train on a GPU.

**Chinese:** 將專案clone下來後，執行**model_training/agc_training.py** 即可開始訓練。若訓練好想要測試結果，可在執player都設定好後，執行**playground.py**。

訓練過程可能會花上較長一段時間，因為AI需訓練大約4000+場後才會逐漸有成果。建議使用GPU來跑訓練。
