

from random import randint
import cv2
import numpy as np
from ultralytics import YOLO

class File:
    def __init__(self, name: str, mode: str):
        self.__name: str = name
        self.__mode: str = mode
        self.file = self.open()
        self.data = self.read()
        self.classes: [str] = self.data.split("\n")
        self.yolo_model = YOLO("weights/yolov8n.pt", "v8")

    @property
    def name(self) -> str:
        return self.__name
    
    @name.setter
    def name(self, value) -> None:
        self.__name = value

    @property
    def mode(self) -> str:
        return self.__mode
    
    @mode.setter
    def mode(self, value) -> None:
        self.mode = value
    
    def open(self):
        self.file = open(self.name, self.mode)
        return self.file
    
    def read(self):
        self.data = self.file.read()
        return self.data
    
    def close(self):
        self.file.close()

class Tool:
    def __init__(self,):
        pass
    
    @staticmethod
    def get_color() -> int:
        return randint(0, 255)

    def set_group_color_pallet(self, size:int) -> [int]:
        color_box: [int] = []
        
        for i in range(size):
            color_box.append(self.set_color_pallet())
        
        return color_box
    
    def set_color_pallet(self):
        return (self.get_color(), self.get_color(), self.get_color())

class Monitor:
    def __init__(self, x:int, y: int):
        self.__x = x
        self.__y = y
    
    @property
    def x(self) -> int:
        return self.__x
    
    @x.setter
    def x(self, value) -> None:
        self.__x = value

    @property
    def y(self) -> int:
        return self.__y
    
    @y.setter
    def y(self, value) -> None:
        self.__y = value

class Camera:
    def __init__(self, file: File, tool: Tool, monitor: Monitor, ip_address: str):
        self.file: File = file  # contêm os arquivos da classe de objetos
        self.tool: Tool = tool  # ferramenta externa usadas
        self.monitor: Monitor = monitor
        self.ip_address: str = ip_address
        self.people: int = 0
        # Uma cor p/ cada moldura de detecção que contorna um objeto (passa o tamanho do array das classes)
        self.color_box = self.tool.set_group_color_pallet(len(self.file.classes))
        self.video = cv2.VideoCapture("http://" + self.ip_address + "/video")
        self.font = cv2.FONT_HERSHEY_COMPLEX
        self.rectangle = None
        self.frame = None
        self.predict = None
        self.report = None

        # Em atribs: bottom_left_x, bottom_left_y, top_right_x, top_right_y
        # Tentei ajustar "atribs" p/ dicionário aninhado e obtive erro, então mantenho como tupla
        self.properties: dict = {"class_id": "", "confidence": 0, "atribs": (0, 0, 0, 0)}
    
        self.run()
    
    def run(self):
        self.file.open()
        self.file.read()
        print(self.file.classes)
        self.file.close()
        
        # Variáveis p/ add legibilidade
        middle_screen: int = self.monitor.x // 2
        pixels_away_from_top: int  = 30
        
        if not self.video.isOpened():
            print("Cannot open camera")
            exit(0)

        while True:
            self.rectangle, self.frame = self.video.read()

            if not self.rectangle:
                print("Quadro não pôde ser exibido (encerrando)...")
                break
            
            self.change_frame_size(self.monitor.x, self.monitor.y)

            self.predict = self.file.yolo_model.predict(source=[self.frame], conf=0.45, save=False)

            self.detection_report = self.predict[0].numpy()

            if len(self.detection_report) != 0:
                for i in range(len(self.predict[0])):
                    self.report = self.predict[0].boxes
                    box_properties = self.report[i]
                    self.properties["class_id"] = box_properties.cls.numpy()[0]
                    self.properties["confidence"] = box_properties.conf.numpy()[0]
                    self.properties["atribs"] = box_properties.xyxy.numpy()[0]
                    
                    self.draw(frame_thickness=3)
                    
                    complement: str = " " + str(round(self.properties["confidence"], 3)) + "%"
                    
                    # Resultado da detecção de outros objetos na tela
                    self.display(
                        font_label=self.file.classes[int(self.properties["class_id"])] + complement,
                        font_pos=(
                            int(self.properties["atribs"][0]), 
                            int(self.properties["atribs"][1]) - 10
                        ),
                        font_size=0.7,
                        font_color=self.tool.set_color_pallet(), 
                        font_thickness=2
                    )

                    self.person_countage()
                    
                    # Quando algo é detectado na tela (mostra resultados no terminal)
                    print("--o A", self.properties["class_id"])
                    print("--o B", self.properties["confidence"])
                    print("--o C", self.properties["atribs"])

            # Resultado da detecção da pessoa na tela
            self.display(
                font_label="Pessoas: " + str(self.people),
                font_pos=(middle_screen, pixels_away_from_top),
                font_size=1,
                font_color=(0, 0, 255),
                font_thickness=2
            )
    
            self.people = 0      
            self.enable()
            self.interrupt()
            
        print("fim...")

    def change_frame_size(self, x: int, y: int) -> None:
        self.frame = cv2.resize(self.frame, (x, y))
    
    def enable(self) -> None:
        cv2.imshow("Câmera", self.frame)
    
    def draw(self, frame_thickness: int)-> None:
        cv2.rectangle(
            self.frame,
            (int(self.properties["atribs"][0]), int(self.properties["atribs"][1])),
            (int(self.properties["atribs"][2]), int(self.properties["atribs"][3])),
            self.color_box[int(self.properties["class_id"])],
            frame_thickness,
        )
    
    def display(self, font_label: str, font_pos: tuple, font_size: int, font_color: tuple, font_thickness: int) -> None:
        # img, text, org, fontFace, fontScale, color, thickness (do texto)
        cv2.putText(
            self.frame,
            font_label,
            (font_pos[0], font_pos[1]),
            self.font,
            font_size,
            font_color,
            font_thickness,
        )

    def person_countage(self) -> None:
        if self.file.classes[int(self.properties["class_id"])] == "person": self.people += 1

    @staticmethod
    def interrupt() -> None: 
        if cv2.waitKey(1) == ord("q"):
            exit(0)

if __name__ == "__main__":
    ip_address: str = "192.168.3.179:4747"
    classes_path: str = "cls.txt"
    read_mode: str = "r"
    tool: Tool = Tool()
    monitor: Monitor = Monitor(x=1024, y=600)
    file = File(name=classes_path, mode=read_mode)
    camera = Camera(file=file, tool=tool, monitor=monitor, ip_address=ip_address)
