# SLP课程设计-音准检测系统

## 文件说明

- singing_score_calculation
  - UI.py：编写了UI界面，并调用了其他的py文件
  - sqc_comparison.py：定义了评分函数
  - dtw_music.py：定义了dtw算法对用户评分的函数
  - mp3towav.py：mp3文件转成wav文件
  - play.py：音频播放程序
  - record.py：音频录制程序
  - play_record.py：并发播放及录制的程序
  - show_lrc_with_time.py：随时间展示歌词的程序
  - Stop_Thread.py：强制停止线程的程序
  - wav2midi.exe：编译好的可执行文件，可以将wav文件转为midi文件
  - test.wav：临时保存的用户现场歌唱的音频
  - test.mid：临时保存的用户现场歌唱的主旋律导出的midi文件
  - timg1.jpg：界面的背景图片
- oursong：提前录制好的一部分唱歌音频，主要用来测试程序功能
- mp3：程序包含的可以用来跟唱的MP3片段
- wavsong：程序包含的可以用来跟唱的MP3片段对应的wav片段
- wavbanzou：提取的纯伴奏音频
- yuanchang：提取的去除伴奏音频，保留了原唱，可以用来提取主旋律与用户做比较
- template_sqnc：保存了原唱提取主旋律得到的midi文件
- melody：用户上传的更多文件提取得到的midi文件的保存位置
- lrc：保存带时间歌词文件
- requirements.txt：和程序运行相关的包

## 运行方式

pip install -r requirements.txt<br>

cd ./singing_score_calculation<br>

python UI.py<br>

