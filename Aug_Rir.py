import numpy as np
import pyroomacoustics as pra
import soundfile as sf
import random
import os
"""
 参考博客：
 https://www.cnblogs.com/tingweichen/p/13861569.html
"""

if __name__ == '__main__':
    for i in range(50):
        # 创建2D房间尺寸,房间的四个角
        a = random.randint(20, 60)
        b = random.randint(1, 60)
        corner = np.array([[0, 0], [a, 0], [a, b], [0, b]]).T
        # corner = np.array([[0, 0], [7, 0], [7, 5], [0, 5]]).T
        # 文档中表示四个角的声明顺序必须逆时针
        room = pra.Room.from_corners(corner)

        # 房间加维度
        room.extrude(3.)

        audio, sr = sf.read('s1r2_0_1_1.wav')

        # 圆点表示设置的声源位置，叉叉表示麦克风的位置。这里设置了三个麦克风
        room = pra.Room.from_corners(corner, fs=sr,
                                 max_order=3,
                                 materials=pra.Material(0.2, 0.15),
                                 ray_tracing=True, air_absorption=True)
        room.add_source([1, 1], signal=audio)

        R = pra.circular_2D_array(center=[2., 2.], M=3, phi0=0, radius=0.3)
        room.add_microphone_array(pra.MicrophoneArray(R, room.fs))

        room.image_source_model()
        # 通过simulate()方法可以查看经过RIR后的语音以及保存语音
        room.simulate()
        rir_name = "length_{}_wide_{}_aug_rir.wav".format(a, b)
        print(rir_name)
        """
            新生成的rir地址,可以将其修改为自己想要保存的文件的文件夹
        """
        save_rir_path = "/data2/wzd/virtual_rir/aug_rir/"
        sf.write(save_rir_path + str(rir_name), room.mic_array.signals.T, samplerate=sr)
        path = os.listdir(save_rir_path)
    print("----------Sava_Finished--------------")
    file = os.listdir(save_rir_path)

    """
        下面的循环的作用是利用linux sox方法将多通道的wav转化为单通道的wav
    """
    for temp in file:
        save_rir_path = "/data2/wzd/virtual_rir/aug_rir/"
        single_file = "single" +"_"+ str(temp)
        os.system('cd {} ; sox {} -c1 {}; rm -rf {}'.format(save_rir_path, temp, single_file, temp))

    print("-----—Single_Save__Finished-------")









