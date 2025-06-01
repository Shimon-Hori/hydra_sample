# hydra_sample

- 公式ドキュメント：<https://hydra.cc/docs/intro/>

## 実行手順

1. `python3 -m venv ~/.hedra_sample`
2. `source ~/.hydra_sample/bin/activate`
3. `pip install -r requirements.txt`
4. `python main.py`

# 実装方法

## yamlファイルの書き方

### デフォルト設定

  以下のようにしてデフォルトの設定をインポート

`conf/config.yaml`

  ```yaml
  defaults:
    - [フォルダ名]: [yamlファイル名]
    - [フォルダ名]: [yamlファイル名]
    - _self_
  ```

- `_self_`の位置で挙動が異なる
  - _self_が最下部：config.yamlのファイルの設定が他ファイルを上書き
  - _self_が最上部：config.yamlのファイルの設定を他ファイルが上書き
  - <https://hydra.cc/docs/tutorials/basic/your_first_app/defaults/#composition-order-of-primary-config>

### その他の設定

関連したパラメータを一つのファイルやインデントに分ける

```conf/model/detr_action_head.yaml```

```yaml
defaults:
  - default_detr

name: detr_action_head_with_objects

out_image_feat_dim: 5

losses:
  ce_threshold: 0.5
  eos_coefficient: 0.1
  ce_loss_coefficient: 1
  bbox_loss_coefficient: 3
  giou_loss_coefficient: 2
```

## 自分のコードでhydraを実装する手順

1. ライブラリのインストール

```pip install hydra-core --upgrade```

2. `conf`ディレクトリを作成
3. デフォルトの設定を記述する`config.yaml`を作成
4. その他の設定ファイルを作成

- `config.yaml`の`defaults:`に記述することで設定をインポートできる

5. `main`関数にデコレータを追加

```@hydra.main(version_base=None, config_path="conf", config_name="config")```

6. `main`関数を書き換える
```def main(cfg: DictConfig) -> None:```

### 実験ごとにyamlファイルを作成する場合

例: `conf/experiment/debug_ava.yaml`

```yaml
# @package _global_
defaults:
  - override /dataset: ava # データセットごとのデフォルトの設定

# その他の設定
run:
  name: "test"
  tag: "test"
  disable_comet: True
  only_val: False
  save_model_checkpoint: True
  save_checkpoint_dir: "./experiment_logs"
  resume_from_checkpoint: ""
  val_videomap: True
  val_framemap: True

logging:
  num_images_to_visualize: 8
  num_true_tubes_to_visualize: 3
  num_false_tubes_to_visualize: 3
  save_tube_iou_thres: 0.5
  save_made_tubes: false
  log_videomap_summary: True
  draw_no_class_pr_curve: True

```

### 実行方法

```python main.py +[実験ごとのyamlファイルがあるフォルダ名]=[yamlファイル名]```

例: ```python main.py +experiment=debug_ava```

### 注意点

- `# @package _global_`をyamlファイルの先頭に記述することで，別のディレクトリの設定を参照できる
- `override /`で既にある設定を上書きできる
- このサンプルコードでは以下の順で設定が上書きされていく

1. `config.yaml`内の以下の部分

```
  - dataset: jhmdb21
  - model: detr_action_head
  - training: default_training
  - logging: visualization
```

2. `config.yaml`内の以下の部分

```
run:
  name: "test"
  tag: "test"
  disable_comet: False
  only_val: False
  save_model_checkpoint: True
  save_checkpoint_dir: "./experiment_logs"
  resume_from_checkpoint: ""
  val_videomap: True
  val_framemap: True

training:
  num_epochs: 100
  batch_size: 4

evaluation:
  val_epochs: 5
  save_epochs: 5
```

3. experimentで指定した設定
