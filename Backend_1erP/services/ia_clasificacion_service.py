import re
import unicodedata
from typing import List, Dict
from models.enums import NivelPrioridad, FuenteClasificacion


class IAClasificacionService:
    """
    Motor Heurístico de Inteligencia Artificial para Veltra.
    Implementa clasificación por scoring y recomendación multivariable.
    100% backend, sin dependencias de IA cloud ni Ollama.
    """

    # --- Constantes internas de categorías (evitan strings mágicos dispersos) ---
    CAT_MOTOR = "motor"
    CAT_ELECTRICA = "electrica"
    CAT_NEUMATICOS = "neumaticos"
    CAT_FRENOS = "frenos"
    CAT_TRANSMISION = "transmision"
    CAT_CARROCERIA = "carroceria"
    CAT_MECANICA_GENERAL = "mecanica_general"
    CAT_OTRO = "otro"

    # Categorías que siempre requieren técnico especializado
    CATEGORIAS_ESPECIALIZADAS = {CAT_MOTOR, CAT_ELECTRICA, CAT_FRENOS, CAT_TRANSMISION}

    # Fuente de clasificación oficial (alineado con el Enum del modelo)
    FUENTE_HEURISTICA = FuenteClasificacion.reglas_heuristicas

    # Diccionario de pesos por categoría (evita listas de if/elif lineales)
    KEYWORDS_CATEGORIAS: Dict[str, Dict[str, int]] = {
        CAT_MOTOR:           {"motor": 10, "humo": 5, "aceite": 5, "bujia": 8, "calienta": 7,
                              "piston": 10, "valvula": 10, "ruido": 3, "ciguenal": 10},
        CAT_ELECTRICA:       {"bateria": 10, "luces": 5, "alternador": 8, "arranca": 7, "corto": 9,
                              "faro": 4, "tablero": 4, "fusible": 6, "electrico": 6},
        CAT_NEUMATICOS:      {"llanta": 10, "pinchazo": 8, "goma": 7, "rueda": 7, "aire": 5,
                              "clavo": 6, "vibracion": 3, "reventado": 9},
        CAT_FRENOS:          {"freno": 10, "pastilla": 9, "disco": 8, "liquido": 5,
                              "chirrido": 4, "pedal": 6, "abs": 7},
        CAT_TRANSMISION:     {"caja": 10, "cambio": 7, "embrague": 9, "clutch": 9,
                              "marcha": 6, "transmision": 10, "cardan": 8},
        CAT_CARROCERIA:      {"choque": 10, "golpe": 8, "puerta": 6, "parachoques": 7,
                              "vidrio": 5, "pintura": 4, "abolladura": 7, "volco": 10},
        CAT_MECANICA_GENERAL: {"suspension": 8, "amortiguador": 8, "direccion": 7,
                               "alineacion": 5, "mantenimiento": 4},
    }

    # Keywords de gravedad para determinar prioridad y grúa
    _KW_CRITICOS = {"fuego", "choque", "volco", "volcado", "incendio", "explosio"}
    _KW_GRAVES   = {"humo", "frenos", "inmovilizado", "no arranca", "no enciende",
                    "bloqueado", "grua", "remolque", "aceite perdiendo", "chispa"}
    _KW_INMOVILIZADORES = {"no arranca", "no enciende", "bloqueado", "grua", "remolque",
                            "choque", "fuego", "volcado", "llanta destruida", "reventado",
                            "volco", "inmovilizado"}

    def _normalizar(self, texto: str) -> str:
        if not texto:
            return ""
        texto = "".join(
            c for c in unicodedata.normalize("NFD", texto)
            if unicodedata.category(c) != "Mn"
        )
        texto = texto.lower()
        texto = re.sub(r"[^a-z0-9\s]", "", texto)
        return " ".join(texto.split())

    def clasificar_incidente(
        self, descripcion: str, archivos_metadata: List[Dict], contexto: Dict
    ) -> Dict:
        desc = self._normalizar(descripcion)

        # 1. Scoring de categorías
        scores: Dict[str, int] = {cat: 0 for cat in self.KEYWORDS_CATEGORIAS}
        for cat, keywords in self.KEYWORDS_CATEGORIAS.items():
            for kw, peso in keywords.items():
                if kw in desc:
                    scores[cat] += peso

        max_score = max(scores.values()) if scores else 0
        categoria = self.CAT_OTRO if max_score == 0 else max(scores, key=scores.get)

        # 2. Subcategoría: primera keyword con mayor peso presente en el texto
        subcategoria = "indeterminado"
        if max_score > 0:
            kw_match = sorted(
                [k for k in self.KEYWORDS_CATEGORIAS[categoria] if k in desc],
                key=lambda k: self.KEYWORDS_CATEGORIAS[categoria][k],
                reverse=True,
            )
            subcategoria = f"falla_en_{kw_match[0]}" if kw_match else "falla_detectada"

        # 3. Prioridad — usando Enum oficial
        prioridad = NivelPrioridad.baja
        if any(kw in desc for kw in self._KW_CRITICOS):
            prioridad = NivelPrioridad.critica
        elif any(kw in desc for kw in self._KW_GRAVES):
            prioridad = NivelPrioridad.alta
        elif max_score > 15:
            prioridad = NivelPrioridad.media

        # 4. Requiere grúa — inferido por keywords de inmovilización
        requiere_grua = any(kw in desc for kw in self._KW_INMOVILIZADORES)

        # 5. Requiere técnico especializado — por categoría ganadora o score alto
        requiere_especialista = (
            categoria in self.CATEGORIAS_ESPECIALIZADAS or max_score > 20
        )

        # 6. Confianza heurística calculada (0.10 – 0.95)
        num_señales = sum(
            1 for cat in self.KEYWORDS_CATEGORIAS
            for kw in self.KEYWORDS_CATEGORIAS[cat]
            if kw in desc
        )
        confianza = min(0.40, num_señales * 0.08) + min(0.40, max_score / 55.0)
        if archivos_metadata:
            confianza += 0.10   # evidencia adjunta
        if contexto.get("vehiculo_id"):
            confianza += 0.05   # vehículo identificado
        confianza = round(min(0.95, confianza if num_señales > 0 else 0.10), 2)

        # 7. Observaciones textuales
        partes_obs = [f"Analisis heuristico con {num_señales} senales detectadas."]
        if num_señales == 0:
            partes_obs.append("Descripcion vaga: revision manual recomendada.")
        elif confianza < 0.40:
            partes_obs.append("Confianza baja por ambiguedad.")
        if archivos_metadata:
            partes_obs.append(f"Se registraron {len(archivos_metadata)} archivos como evidencia.")
        if contexto.get("marca"):
            partes_obs.append(f"Vehiculo: {contexto['marca']} {contexto.get('modelo', '')}.")

        return {
            "categoria_incidente":          categoria,
            "subcategoria_incidente":       subcategoria,
            "nivel_prioridad":              prioridad.value,
            "requiere_grua":                requiere_grua,
            "requiere_tecnico_especializado": requiere_especialista,
            "observaciones_modelo":         " ".join(partes_obs),
            "confianza_modelo":             confianza,
            "fuente_clasificacion":         self.FUENTE_HEURISTICA.value,
        }

    def recomendar_sucursales(
        self, solicitud_id: int, clasificacion: Dict, sucursales_disponibles: List[Dict]
    ) -> List[Dict]:
        """
        Genera recomendaciones ordenadas por score multivariable.
        Retorna lista vacía si no hay sucursales válidas.
        """
        req_especialista = clasificacion.get("requiere_tecnico_especializado", False)
        prioridad_val    = clasificacion.get("nivel_prioridad", NivelPrioridad.baja.value)
        es_prioridad_alta = prioridad_val in (NivelPrioridad.alta.value, NivelPrioridad.critica.value)

        recomendaciones = []

        for suc in sucursales_disponibles:
            if not suc.get("disponible", True):
                continue

            score_total  = 0.0
            justificacion: List[str] = []
            criterios: Dict = {
                "disponibilidad_servicio":       True,
                "requiere_tecnico_especializado": req_especialista,
            }

            # ---- Distancia (Max 35 pts) ----
            distancia = suc.get("distancia_km")
            if distancia is not None and distancia >= 0:
                criterios["distancia_evaluada"] = True
                criterios["distancia_km"] = round(distancia, 2)
                if distancia <= 2.0:
                    score_dist = 35.0
                    justificacion.append("Muy cercana.")
                elif distancia <= 10.0:
                    score_dist = max(0.0, 35.0 - (distancia * 2.5))
                    justificacion.append("Ubicacion accesible.")
                else:
                    score_dist = max(0.0, 10.0 - (distancia / 5.0))
                    justificacion.append("Sucursal distante.")
                criterios["score_distancia"] = round(score_dist, 2)
                score_total += score_dist
            else:
                # Sin coordenadas: NO se premia la cercanía
                criterios["distancia_evaluada"] = False
                criterios["score_distancia"]    = 0
                justificacion.append("Distancia no evaluada por falta de coordenadas.")

            # ---- Precio (Max 25 pts) ----
            precio = suc.get("precio_local")
            if precio is not None and precio > 0:
                criterios["precio_evaluado"] = True
                criterios["precio_local"]    = precio
                if precio < 150:
                    score_precio = 25.0
                elif precio < 400:
                    score_precio = 15.0
                else:
                    score_precio = 5.0
                criterios["score_precio"] = score_precio
                score_total += score_precio
                if score_precio >= 15:
                    justificacion.append("Precio competitivo.")
            else:
                criterios["precio_evaluado"] = False
                criterios["score_precio"]    = 0
                justificacion.append("Precio no disponible para evaluacion.")

            # ---- Capacidad técnica (Max 30 pts) ----
            tecnicos = suc.get("tecnicos_activos", 0)
            criterios["tecnicos_en_sucursal"] = tecnicos
            if req_especialista:
                if tecnicos > 0:
                    score_tecnico = 30.0
                    justificacion.append("Cuenta con tecnicos activos.")
                else:
                    score_tecnico = 5.0
                    justificacion.append("Advertencia: sin tecnicos activos detectados.")
            else:
                score_tecnico = 20.0 if tecnicos > 0 else 10.0
            criterios["score_capacidad_tecnica"] = score_tecnico
            score_total += score_tecnico

            # ---- Bono de prioridad (Max 10 pts) ----
            if es_prioridad_alta:
                criterios["bono_prioridad"] = 10
                score_total += 10.0
            else:
                criterios["bono_prioridad"] = 0

            final_score = round(min(100.0, score_total), 2)
            criterios["score_total"] = final_score

            recomendaciones.append({
                "solicitud_id":               solicitud_id,
                "sucursal_recomendada_id":    suc["sucursal_id"],
                "score_recomendacion":        final_score,
                "criterios_evaluados":        criterios,
                "justificacion_recomendacion": " ".join(justificacion) if justificacion
                                               else "Sucursal apta.",
                "precio_estimado":            precio if precio else 0.0,
                "distancia_estimada":         distancia if distancia is not None else 0.0,
            })

        recomendaciones.sort(key=lambda x: x["score_recomendacion"], reverse=True)
        return recomendaciones
