# MP4视频格式
Mp4格式是一个个Box，其中**moov**存储的是metadata信息，**mdat**存储具体音视频数据信息。**如果无法解析出moov数据，是无法播放该mp4文件的**。而一般情况下ffmpeg生成moov是在mdat写入完成之后的，即mdat会在moov的前面,如图：

<img src=res/mp4.png alt="mp4文件结构"/>

### [qtfaststart2](https://github.com/danielyaa5/qtfaststart2) 查看mp4文件moov的位置
```bash
# 先安装
pip install qtfaststart2

# 查看 moov的位置
qtfaststart2 -l a.mp4
```
注意：这里用的是 **qtfaststart2**(中间没有 **-** ) 不是 **qt-faststart**， **qt-faststart**不能查看moov的位置，下面有介绍。qtfaststart2 -l a.mp4  命令输出如下：
<pre>
$ qtfaststart2 -l a.mp4
    ftyp (32 bytes)
    moov (8311 bytes)  <--可以看到这个mp4文件的 moov 位置不在后面 
    free (8 bytes)
    mdat (11154820 bytes)
</pre>


### 秒开方式一： `moov`移前（还是比不上`m3u8`)
MP4文件在播放时，ftyp与moov需同时加载完成后，并下载部分mdat的帧数据后，才能开始播放。在播放moov在后面的MP4时，会严重影响用户体验，因为需要加载整个视频，才能获得moov信息后，视频才能播放。针对这种情况，通用的做法是在服务端做处理。**通过ffmpeg命令吧moov移动到mdat前面， 这样视频可以尽快播放，而不用等到整个视频加载完（秒开）**

#### 1. 使用ffmpeg把moov前移
```bash
 ffmpeg -i in.mp4 -c copy -f mp4 -movflags faststart out.mp4
```
-  **`-c copy`** (或者 **`-codec copy`**) 选项表示复制音视频数据，不做任何编码或转码。需要注意的是，-codec copy选项只适用于输入文件和输出文件的编解码格式相同的情况。如果你需要将一个编码格式不同的音视频文件复制为另一种编码格式，需要使用其他的编码器或转码器进行操作。
- **`-f mp4`** 强制指定输入文件的格式是MP4格式

#### 2. qt-faststart把moov前移
**qt-faststart 在安装ffmpeg的时候，会自动安装。** 它是一个由Mike Melanson (melanson@pcisys.net)写的开源程序，是一个命令行工具。你可能可以在很多地方找到它的源码，一般是在FFmpeg的源码中拿，它通常放在FFmpeg源码的tools目录下，比如github仓库中的位置为https://github.com/FFmpeg/FFmpeg/blob/master/tools/qt-faststart.c。该程序只有一个源码文件，很小（不到13KB）

qt-faststart的使用十分简单，其调用格式为：
```bash
# in.mp4文件保持不变， 把in.mp4的moov前移后，并生成新的文件out.mp4
qt-faststart in.mp4  out.mp4
```
mp4文件也可以替换为mov文件，因为这个工具其实最开始是为QuickTime格式视频文件编写的

## mp4转为 ts 格式（此步骤可忽略）

```bash
# h264: h264_mp4toannexb
# h265: hevc_mp4toannexb
ffmpeg -y -i move.mp4 -vcodec copy -acodec copy -vbsf hevc_mp4toannexb move.ts


ffmpeg -i filename.mp4 -codec: copy -start_number 0 -hls_time 10 -hls_list_size 0 -f hls filename.m3u8

```

