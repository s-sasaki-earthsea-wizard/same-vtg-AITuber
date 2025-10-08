# ライブ配信を実行するプログラムです。

import os
from talker import Talker
from OBSAdapter import OBSAdapter
from VoiceMaker import VoiceIO, VoiceMaker
from youtube_comment_adapter import YoutubeCommentAdapter
from PlaySound import PlaySound
from dotenv import load_dotenv
import time
import random
load_dotenv(override=True)


class AItuberSystem:
    def __init__(self):
        self.talker = Talker()
        self.obs_adapter = OBSAdapter()
        self.voice_maker = VoiceMaker()
        self.youtubr_comment_adapter = YoutubeCommentAdapter(
            os.environ.get("YOUTUBE_VIDEO_ID"))
        self.play_sound = PlaySound()
        self.last_talk = None  # 最後の発言を保存する変数
        
    def start(self):
        while True:
            comment = self.youtubr_comment_adapter.get_comment()
            if comment is None:
                # talker.pyの話題からランダムに話す
                generater = [self.talker.generate_fairy_tale(), self.talker.generate_about_diary(), 
                             self.talker.drinker_common_things(), self.talker.my_theory_about_music(),
                             self.talker.expand_previous_topic(self.last_talk)]  # last_talkを渡す
                talk = random.choice(generater)
                self.last_talk = talk  # 発言を保存
                talk_list = self.split_text(talk)
                for talk in talk_list:
                    voice: VoiceIO = self.voice_maker.make_voice_voicevox(talk)
                    self.obs_adapter.set_question("")
                    self.obs_adapter.set_answer(talk)
                    self.play_sound.play_sound(voice)
            else:
                character_speak = self.talker.chat(comment)
                self.last_talk = character_speak  # 発言を保存
                speak_list = self.split_text(character_speak)
                for speak in speak_list:
                    voice: VoiceIO = self.voice_maker.make_voice_voicevox(speak)
                    self.obs_adapter.set_question(comment)
                    self.obs_adapter.set_answer(speak)
                    self.play_sound.play_sound(voice)
            time.sleep(1)
    
    def split_text(self, text: str) -> list[str]:
        # 。を区切りにしてリストにする
        text = text.replace("\n", "")
        return text.split("。")


if __name__ == "__main__":
    aituber_system = AItuberSystem()
    aituber_system.start()