import random
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from panda3d.core import (
    AmbientLight, DirectionalLight, Vec4, Vec3, WindowProperties,
    CardMaker, TextNode, ClockObject
)
from direct.gui.OnscreenText import OnscreenText

class TrafficRider(ShowBase):
    def __init__(self):
        super().__init__()

        # --- 1. CONFIGURACIÓN DE VENTANA ---
        self.disableMouse()
        props = WindowProperties()
        props.setTitle("Traffic Rider 3D - Python Panda3D")
        props.setSize(1280, 720)
        self.win.requestProperties(props)
        self.setBackgroundColor(0.4, 0.6, 0.9, 1.0)  # Cielo azul

        # --- 2. CONTROLES Y ESTADO DE JUEGO ---
        self.keys = {"left": False, "right": False, "accelerate": False, "brake": False}
        self.registrar_controles()

        self.game_over = False
        self.distancia_recorrida = 0.0
        self.velocidad_actual = 20.0
        self.velocidad_maxima = 120.0
        self.velocidad_minima = 20.0
        self.aceleracion = 35.0
        self.frenado = 60.0

        # --- 3. CREACIÓN DEL ESCENARIO (CARRETERA) ---
        self.ancho_carril = 4.0
        self.carriles = [-6.0, -2.0, 2.0, 6.0]
        self.crear_carretera()

        # --- 4. JUGADOR (MOTO / CÁMARA PRIMERA PERSONA) ---
        self.moto_x = -2.0
        self.moto_z = 1.2
        self.velocidad_lateral = 12.0

        self.crear_manillar()

        # --- 5. SISTEMA DE TRÁFICO ---
        self.trafico = []
        self.tiempo_ultimo_spawn = 0

        # --- 6. INTERFAZ DE USUARIO ---
        self.hud_velocidad = OnscreenText(
            text="0 KM/H", pos=(-0.95, 0.85), scale=0.08,
            fg=(1, 1, 0, 1), align=TextNode.ALeft, mayChange=True
        )
        self.hud_distancia = OnscreenText(
            text="0 M", pos=(-0.95, 0.75), scale=0.06,
            fg=(1, 1, 1, 1), align=TextNode.ALeft, mayChange=True
        )
        self.hud_gameover = OnscreenText(
            text="", pos=(0, 0), scale=0.12,
            fg=(1, 0.2, 0.2, 1), align=TextNode.ACenter, mayChange=True
        )

        # --- 7. ILUMINACIÓN ---
        self.configurar_luces()

        self.taskMgr.add(self.actualizar_juego, "BucleTrafficRider")

    def registrar_controles(self):
        teclas = [
            ("arrow_left", "left", True), ("arrow_left-up", "left", False),
            ("a", "left", True), ("a-up", "left", False),
            ("arrow_right", "right", True), ("arrow_right-up", "right", False),
            ("d", "right", True), ("d-up", "right", False),
            ("arrow_up", "accelerate", True), ("arrow_up-up", "accelerate", False),
            ("w", "accelerate", True), ("w-up", "accelerate", False),
            ("arrow_down", "brake", True), ("arrow_down-up", "brake", False),
            ("s", "brake", True), ("s-up", "brake", False),
            ("r", "restart", True)
        ]
        for evento, accion, estado in teclas:
            if accion == "restart":
                self.accept(evento, self.reiniciar_juego)
            else:
                self.accept(evento, self.actualizar_tecla, [accion, estado])

    def actualizar_tecla(self, accion, estado):
        self.keys[accion] = estado

    def crear_carretera(self):
        cm = CardMaker('asfalto')
        cm.setFrame(-10, 10, 0, 300)
        self.asfalto = self.render.attachNewNode(cm.generate())
        self.asfalto.setPos(0, 0, 0)
        self.asfalto.setP(-90)
        self.asfalto.setColor(0.15, 0.15, 0.18, 1.0)

        cm_grass = CardMaker('hierba')
        cm_grass.setFrame(-100, 100, 0, 300)
        self.hierba = self.render.attachNewNode(cm_grass.generate())
        self.hierba.setPos(0, 0, -0.05)
        self.hierba.setP(-90)
        self.hierba.setColor(0.1, 0.4, 0.1, 1.0)

        self.lineas_carril = []
        for x in [-4.0, 0.0, 4.0]:
            for z in range(0, 300, 10):
                linea_cm = CardMaker('linea')
                linea_cm.setFrame(-0.15, 0.15, 0, 5)
                linea = self.render.attachNewNode(linea_cm.generate())
                linea.setPos(x, z, 0.02)
                linea.setP(-90)
                linea.setColor(1, 1, 1, 1)
                self.lineas_carril.append(linea)

    def crear_manillar(self):
        cm = CardMaker('manillar')
        cm.setFrame(-0.8, 0.8, -0.4, 0.2)
        self.manillar = self.aspect2d.attachNewNode(cm.generate())
        self.manillar.setPos(0, 0, -0.7)
        self.manillar.setColor(0.1, 0.1, 0.1, 1.0)

    def configurar_luces(self):
        luz_amb = AmbientLight('amb')
        luz_amb.setColor(Vec4(0.4, 0.4, 0.5, 1.0))
        self.render.setLight(self.render.attachNewNode(luz_amb))

        luz_dir = DirectionalLight('dir')
        luz_dir.setColor(Vec4(0.9, 0.85, 0.8, 1.0))
        nodo_dir = self.render.attachNewNode(luz_dir)
        nodo_dir.setHpr(-30, -60, 0)
        self.render.setLight(nodo_dir)

    def spawn_vehiculo(self):
        carril_x = random.choice(self.carriles)
        velocidad_vehiculo = random.uniform(15.0, 35.0)

        cm = CardMaker('coche')
        cm.setFrame(-1.2, 1.2, 0, 4.5)
        coche_node = self.render.attachNewNode("Coche")

        cuerpo = coche_node.attachNewNode(cm.generate())
        cuerpo.setP(-90)
        cuerpo.setZ(0.8)

        color = random.choice([
            Vec4(0.8, 0.1, 0.1, 1),
            Vec4(0.1, 0.3, 0.8, 1),
            Vec4(0.9, 0.9, 0.1, 1),
            Vec4(0.8, 0.8, 0.8, 1)
        ])
        cuerpo.setColor(color)

        coche_node.setPos(carril_x, 250, 0)

        self.trafico.append({
            "nodo": coche_node,
            "velocidad": velocidad_vehiculo,
            "carril": carril_x
        })

    def actualizar_juego(self, tarea):
        # CAMBIO 1
        dt = ClockObject.getGlobalClock().getDt()

        if dt == 0 or self.game_over:
            return Task.cont

        # --- A) ACELERACIÓN Y VELOCIDAD DE LA MOTO ---
        if self.keys["accelerate"]:
            self.velocidad_actual = min(
                self.velocidad_maxima,
                self.velocidad_actual + self.aceleracion * dt
            )
        elif self.keys["brake"]:
            self.velocidad_actual = max(
                self.velocidad_minima,
                self.velocidad_actual - self.frenado * dt
            )
        else:
            if self.velocidad_actual > 40.0:
                self.velocidad_actual -= 10.0 * dt

        self.distancia_recorrida += (
            self.velocidad_actual * 0.27778
        ) * dt

        # --- B) CONTROL LATERAL DE LA MOTO ---
        inclinacion = 0.0

        if self.keys["left"]:
            self.moto_x = max(
                -8.5,
                self.moto_x - self.velocidad_lateral * dt
            )
            inclinacion = -5.0

        if self.keys["right"]:
            self.moto_x = min(
                8.5,
                self.moto_x + self.velocidad_lateral * dt
            )
            inclinacion = 5.0

        self.camera.setPos(self.moto_x, 0, self.moto_z)
        self.camera.setHpr(0, -2, inclinacion)

        # --- C) MOVER LÍNEAS DE CARRETERA ---
        desplazamiento_carretera = self.velocidad_actual * dt

        for linea in self.lineas_carril:
            linea.setY(linea.getY() - desplazamiento_carretera)

            if linea.getY() < 0:
                linea.setY(linea.getY() + 300)

        # --- D) GESTIÓN DE TRÁFICO ---

        # CAMBIO 2
        if ClockObject.getGlobalClock().getFrameTime() - self.tiempo_ultimo_spawn > max(
            0.6,
            2.5 - (self.velocidad_actual / 80.0)
        ):
            self.spawn_vehiculo()

            # CAMBIO 3
            self.tiempo_ultimo_spawn = ClockObject.getGlobalClock().getFrameTime()

        for vehiculo in self.trafico[:]:
            nodo = vehiculo["nodo"]

            v_relativa = self.velocidad_actual - vehiculo["velocidad"]
            nodo.setY(
                nodo.getY() - v_relativa * dt * 0.5
            )

            dist_y = nodo.getY() - self.camera.getY()
            dist_x = abs(nodo.getX() - self.moto_x)

            if 0.0 < dist_y < 3.5 and dist_x < 1.4:
                self.finalizar_juego()

            if nodo.getY() < -10:
                nodo.removeNode()
                self.trafico.remove(vehiculo)

        # --- E) ACTUALIZAR HUD ---
        self.hud_velocidad.setText(
            f"{int(self.velocidad_actual)} KM/H"
        )
        self.hud_distancia.setText(
            f"{int(self.distancia_recorrida)} M"
        )

        return Task.cont

    def finalizar_juego(self):
        self.game_over = True
        self.hud_gameover.setText(
            "¡CHOQUE!\nPresiona 'R' para reiniciar"
        )

    def reiniciar_juego(self, estado):
        if not self.game_over or not estado:
            return

        for v in self.trafico:
            v["nodo"].removeNode()

        self.trafico.clear()

        self.moto_x = -2.0
        self.velocidad_actual = 20.0
        self.distancia_recorrida = 0.0
        self.game_over = False
        self.hud_gameover.setText("")


if __name__ == "__main__":
    app = TrafficRider()
    app.run()