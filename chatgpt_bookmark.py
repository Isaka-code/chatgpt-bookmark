from pychatgpt import Chat, Options
import os
import datetime

class Chat(Chat):
    """
    PyChatGPTパッケージのChatクラスを継承し、以下の機能を加える
    ・ログ保存の日本語への対応（そのままだと文字化けしてしまうため）
    ・終了時に「ブックマークが保存されました」というメッセージを表示する
    """
    def save_data(self):
        """
        ログを保存するsave_dataメソッドをオーバーライドし、encoding="utf-8"に変更することで日本語に対応させる
        """
        if self.options.track:
            try:
                with open(self.options.chat_log, "a", encoding="utf-8") as f:
                    f.write("\n".join(self.__chat_history) + "\n")

                with open(self.options.id_log, "w") as f:
                    f.write(str(self.previous_convo_id) + "\n")
                    f.write(str(self.conversation_id) + "\n")

            except Exception as ex:
                self.log(f"{Fore.RED}>> Failed to save chat and ids to chat log and id_log."
                      f"{ex}")
            finally:
                self.__chat_history = []

    def __del__(self):
        """
        デストラクタに終了時メッセージの表示を追加
        """
        print("ブックマークが保存されました")


def chat(log_path):
    """
    ChatGPTを呼び出すメインルーチン
    """
    options = Options()
    options.track = True
    options.chat_log = log_path

    # emailとpasswordはOpenAIに登録したものを入力してください。
    email = "your_mail@gmail.com"
    password = "your_password"
    chat = Chat(email=email, password=password, options=options)
    chat.cli_chat()

def main(dir_path="bookmarks"):
    # ブックマークを保存するディレクトリを作成
    os.makedirs(dir_path, exist_ok=True)

    # ブックマークのファイル名を作成する
    dt_now = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S') # 現在の時刻
    name = dt_now + "_" + input("ブックマーク名を入力してください：現在の時刻_ブックマーク名.txt\n") + ".txt" # 現在の時刻_ブックマーク名.txt
    
    # ログの保存先
    log_path = os.path.join(dir_path, name) 

    # ChatGPTのメインルーチンを呼び出す
    chat(log_path=log_path)


if __name__ == "__main__":
    main()
