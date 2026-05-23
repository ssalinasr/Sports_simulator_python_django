update "TeamSports" set team_sport_rules = '{
  "sport": "Atletismo",
  "disciplines": {
    "heptathlon": {
      "name": "Heptatlón",
      "scoring_rules": {
        "running_events": {
          "formula": "A*(B-T)^C",
          "variables": {
            "T": "Tiempo realizado"
          }
        },
        "jumping_events": {
          "formula": "A*(M-B)^C",
          "variables": {
            "M": "Marca realizada"
          }
        },
        "throwing_events": {
          "formula": "A*(D-B)^C",
          "variables": {
            "D": "Distancia realizada"
          }
        }
      },
      "events": [
        {
          "name": "200m",
          "category": "running",
          "A": 4.99,
          "B": 42.50,
          "C": 1.81
        },
        {
          "name": "800m",
          "category": "running",
          "A": 0.11,
          "B": 254.00,
          "C": 1.88
        },
        {
          "name": "100m Vallas",
          "category": "running",
          "A": 9.23,
          "B": 26.70,
          "C": 1.84
        },
        {
          "name": "Salto alto",
          "category": "jumping",
          "A": 1.85,
          "B": 75.00,
          "C": 1.35
        },
        {
          "name": "Salto de longitud",
          "category": "jumping",
          "A": 0.19,
          "B": 210.00,
          "C": 1.41
        },
        {
          "name": "Peso",
          "category": "throwing",
          "A": 56.02,
          "B": 1.50,
          "C": 1.05
        },
        {
          "name": "Jabalina",
          "category": "throwing",
          "A": 15.98,
          "B": 3.80,
          "C": 1.04
        }
      ]
    },
    "decathlon": {
      "name": "Decatlón",
      "scoring_rules": {
        "running_events": {
          "formula": "A*(B-T)^C",
          "variables": {
            "T": "Tiempo realizado"
          }
        },
        "jumping_events": {
          "formula": "A*(M-B)^C",
          "variables": {
            "M": "Marca realizada"
          }
        },
        "throwing_events": {
          "formula": "A*(D-B)^C",
          "variables": {
            "D": "Distancia realizada"
          }
        }
      },
      "events": [
        {
          "name": "100m",
          "category": "running",
          "A": 25.43,
          "B": 18.00,
          "C": 1.81
        },
        {
          "name": "Salto de longitud",
          "category": "jumping",
          "A": 0.14,
          "B": 220.00,
          "C": 1.40
        },
        {
          "name": "Peso",
          "category": "throwing",
          "A": 51.39,
          "B": 1.50,
          "C": 1.05
        },
        {
          "name": "Salto de altura",
          "category": "jumping",
          "A": 0.85,
          "B": 75.00,
          "C": 1.42
        },
        {
          "name": "400m",
          "category": "running",
          "A": 1.54,
          "B": 82.00,
          "C": 1.81
        },
        {
          "name": "110m Vallas",
          "category": "running",
          "A": 5.74,
          "B": 28.50,
          "C": 1.92
        },
        {
          "name": "Disco",
          "category": "throwing",
          "A": 12.91,
          "B": 4.00,
          "C": 1.10
        },
        {
          "name": "Salto con pértiga",
          "category": "jumping",
          "A": 0.28,
          "B": 100.00,
          "C": 1.35
        },
        {
          "name": "Jabalina",
          "category": "throwing",
          "A": 10.14,
          "B": 7.00,
          "C": 1.08
        },
        {
          "name": "1500m",
          "category": "running",
          "A": 0.04,
          "B": 480.00,
          "C": 1.85
        }
      ]
    }
  }
}' WHERE team_sport_name = 'Atletismo';

update "TeamSports" set team_sport_rules = '{
  "sport": "Equitacion",
  "disciplines": {
    "individual": {
      "name": "Doma Individual",
      "scoring_rules": {
        "formula": "(T*0.26) + (D*0.26) + (P*0.14) + (S*0.14) + (R*0.10) + (C*0.08) + Random",
        "variables": {
          "T": {
            "name": "Técnica",
            "description": "Calidad técnica general del jinete y el caballo",
            "weight": 0.26
          },
          "D": {
            "name": "Doma",
            "description": "Nivel de control y ejecución de movimientos de doma",
            "weight": 0.26
          },
          "P": {
            "name": "Precisión",
            "description": "Exactitud en la ejecución de figuras y transiciones",
            "weight": 0.14
          },
          "S": {
            "name": "Sincronía",
            "description": "Coordinación y armonía entre jinete y caballo",
            "weight": 0.14
          },
          "R": {
            "name": "Ritmo",
            "description": "Consistencia y regularidad del ritmo durante la presentación",
            "weight": 0.10
          },
          "C": {
            "name": "Concentración",
            "description": "Nivel de enfoque y estabilidad durante la rutina",
            "weight": 0.08
          },
          "Random": {
            "name": "Random",
            "description": "Factor aleatorio adicional para variabilidad de simulación",
            "type": "bonus"
          }
        }
      }
    },
    "free_style": {
      "name": "Doma Libre",
      "scoring_rules": {
        "formula": "(T*0.26) + (C*0.15) + (D*0.26) + (S*0.14) + (R*0.10) + (B*0.09) + Forma + Random",
        "variables": {
          "T": {
            "name": "Técnica",
            "description": "Calidad técnica general del jinete y el caballo",
            "weight": 0.26
          },
          "C": {
            "name": "Creatividad",
            "description": "Originalidad y diseño artístico de la rutina",
            "weight": 0.15
          },
          "D": {
            "name": "Doma",
            "description": "Nivel de control y ejecución de movimientos de doma",
            "weight": 0.26
          },
          "S": {
            "name": "Sincronía",
            "description": "Coordinación y armonía entre jinete y caballo",
            "weight": 0.14
          },
          "R": {
            "name": "Ritmo",
            "description": "Consistencia y fluidez rítmica de la presentación",
            "weight": 0.10
          },
          "B": {
            "name": "Balance",
            "description": "Equilibrio y estabilidad durante la rutina",
            "weight": 0.09
          },
          "Forma": {
            "name": "Forma",
            "description": "Estado general y calidad estética de la presentación",
            "type": "bonus"
          },
          "Random": {
            "name": "Random",
            "description": "Factor aleatorio adicional para variabilidad de simulación",
            "type": "bonus"
          }
        }
      }
    }
  }
}' WHERE team_sport_name = 'Equitacion';

update "TeamSports" set team_sport_rules = '{
  "sport": "Saltos",
  "scoring_rules": {
    "formula": "D * ((J1 + J2 + J3) * 0.6) - S",
    "competition_format": {
      "male": {
        "dives": 6
      },
      "female": {
        "dives": 5
      },
      "mixed": {
        "dives": 6
      }
    },
    "judge_rules": {
      "total_judges": 5,
      "counted_judges": 3,
      "remove_highest": true,
      "remove_lowest": true
    },
    "variables": {
      "D": {
        "name": "Dificultad",
        "description": "Coeficiente de dificultad del salto",
        "range": [1.2, 4.2]
      },
      "J": {
        "name": "Puntaje Juez",
        "description": "Puntaje del juez válido tras eliminar extremos",
        "range": [1, 10]
      },
      "S": {
        "name": "Penalización sincronizada",
        "description": "Deducción aplicada en pruebas sincronizadas",
        "range": [0, 1],
        "optional": true
      }
    }
  }
}' WHERE team_sport_name = 'Saltos';

update "TeamSports" set team_sport_rules = '{
  "sport": "Gimnasia Artística",
  "scoring_rules": {
    "formula": "D + (E - P)",
    "competition_format": {
      "male": {
        "apparatus_count": 5,
        "final_score": "Suma de todas las pruebas"
      },
      "female": {
        "apparatus_count": 4,
        "final_score": "Suma de todas las pruebas"
      }
    },
    "variables": {
      "D": {
        "name": "Dificultad",
        "description": "Valor de dificultad de la rutina",
        "range": [4.5, 7.0]
      },
      "E": {
        "name": "Ejecución",
        "description": "Puntaje base de ejecución que disminuye según errores y deducciones",
        "base_value": 10.0
      },
      "P": {
        "name": "Penalización",
        "description": "Deducciones aplicadas por errores técnicos o infracciones",
        "range": [0.1, 1.0]
      },
      "Total": {
        "name": "Total",
        "description": "Suma de los puntajes obtenidos en todas las pruebas"
      }
    }
  }
}' WHERE team_sport_name = 'Gimnasia Artistica';

update "TeamSports" set team_sport_rules = '{
  "sport": "Gimnasia Rítmica",
  "scoring_rules": {
    "formula": "D + A + (E - P)",
    "competition_format": {
      "apparatus_count": 4,
      "final_score": "Suma de todas las pruebas"
    },
    "variables": {
      "D": {
        "name": "Dificultad",
        "description": "Valor técnico y complejidad de la rutina",
        "range": [12.0, 18.0]
      },
      "A": {
        "name": "Componente Artístico",
        "description": "Calidad artística, musicalidad y expresión de la rutina",
        "range": [6.5, 10.0]
      },
      "E": {
        "name": "Ejecución",
        "description": "Puntaje base de ejecución que disminuye según errores y deducciones",
        "base_value": 10.0
      },
      "P": {
        "name": "Penalización",
        "description": "Deducciones aplicadas por errores técnicos, pérdidas o infracciones",
        "range": [0.1, 1.0]
      },
      "Total": {
        "name": "Total",
        "description": "Suma de los puntajes obtenidos en las cuatro pruebas"
      }
    }
  }
}' WHERE team_sport_name = 'Gimnasia Ritmica';

update "TeamSports" set team_sport_rules = '{
  "sport": "Gimnasia en trampolín",
  "scoring_rules": {
    "formula": "D + (T + H + E + S - P)",
    "variables": {
      "D": {
        "name": "Dificultad",
        "description": "Valor técnico y complejidad de la rutina",
        "range": [13.0, 18.0]
      },
      "E": {
        "name": "Ejecución",
        "description": "Puntaje base de ejecución que disminuye según errores y deducciones",
        "base_value": 10.0
      },
      "T": {
        "name": "Tiempo de Vuelo",
        "description": "Tiempo total que el atleta permanece en el aire durante la rutina",
        "range": [15.0, 18.0]
      },
      "H": {
        "name": "Desplazamiento Horizontal",
        "description": "Control y estabilidad horizontal durante los saltos",
        "range": [15.0, 18.0]
      },
      "P": {
        "name": "Penalización",
        "description": "Deducciones aplicadas por errores técnicos o pérdidas de control",
        "range": [0.1, 1.0]
      },
      "S": {
        "name": "Sincronización",
        "description": "Nivel de sincronía entre atletas en pruebas sincronizadas",
        "range": [7.0, 10.0],
        "optional": true
      }
    }
  }
}' WHERE team_sport_name = 'Gimnasia en Trampolin';

update "TeamSports" set team_sport_rules = '{
  "sport": "Nado Sincronizado",
  "scoring_rules": {
    "technical_routine": {
      "formula": "(0.4*D) + (0.35*E) + (0.15*A) + (0.1*S) - P"
    },
    "free_routine": {
      "formula": "(0.35*D) + (0.25*E) + (0.3*A) + (0.1*S) - P"
    },
    "acrobatics_routine": {
      "formula": "(0.45*D) + (0.2*E) + (0.2*A) + (0.15*S) - P"
    },
    "variables": {
      "D": {
        "name": "Dificultad",
        "description": "Complejidad técnica y física de la rutina",
        "range": [25.0, 40.0]
      },
      "E": {
        "name": "Ejecución",
        "description": "Puntaje base de ejecución que disminuye según errores y deducciones",
        "base_value": 10.0
      },
      "A": {
        "name": "Componente Artístico",
        "description": "Calidad artística, musicalidad y creatividad de la rutina",
        "range": [6.5, 9.0]
      },
      "S": {
        "name": "Sincronización",
        "description": "Nivel de sincronía entre atletas durante la presentación",
        "range": [6.5, 9.0],
        "optional": true
      },
      "P": {
        "name": "Penalización",
        "description": "Deducciones aplicadas por errores técnicos o infracciones",
        "range": [0.1, 1.0]
      }
    }
  }
}' WHERE team_sport_name = 'Nado Sincronizado';

update "TeamSports" set team_sport_rules = '{
  "sport": "Skateboarding",
  "disciplines": {
    "park": {
      "competition_format": {
        "rounds": 3,
        "score_range": [0, 100],
        "final_score": "Suma de las tres rondas"
      },
      "scoring_rules": {
        "formula": "(D*0.25) + (E*0.25) + (A*0.15) + (F*0.15) + (V*0.1) + (O*0.05) + (C*0.05) - P",
        "variables": {
          "D": {
            "name": "Dificultad",
            "description": "Complejidad técnica de los trucos y líneas",
            "weight": 0.25
          },
          "E": {
            "name": "Ejecución",
            "description": "Calidad y limpieza en la ejecución de maniobras",
            "weight": 0.25
          },
          "A": {
            "name": "Amplitud",
            "description": "Altura y alcance de los movimientos",
            "weight": 0.15
          },
          "F": {
            "name": "Flow",
            "description": "Fluidez y continuidad de la ronda",
            "weight": 0.15
          },
          "V": {
            "name": "Variedad",
            "description": "Diversidad de maniobras utilizadas",
            "weight": 0.10
          },
          "O": {
            "name": "Originalidad",
            "description": "Creatividad e innovación en la rutina",
            "weight": 0.05
          },
          "C": {
            "name": "Consistencia",
            "description": "Regularidad y estabilidad durante la ronda",
            "weight": 0.05
          },
          "P": {
            "name": "Penalización",
            "description": "Deducciones por caídas, errores o interrupciones",
            "type": "penalty"
          }
        }
      }
    },
    "street": {
      "competition_format": {
        "runs": 2,
        "tricks": 5,
        "score_range": [0, 100],
        "final_score": "Mejor Run + 2 mejores Tricks"
      },
      "scoring_rules": {
        "formula": "(D*0.2) + (E*0.3) + (F*0.25) + (V*0.15) + (U*0.1) - P",
        "variables": {
          "D": {
            "name": "Dificultad",
            "description": "Complejidad técnica de los trucos",
            "weight": 0.20
          },
          "E": {
            "name": "Ejecución",
            "description": "Calidad y limpieza en la ejecución",
            "weight": 0.30
          },
          "F": {
            "name": "Flow",
            "description": "Fluidez y continuidad de la presentación",
            "weight": 0.25
          },
          "V": {
            "name": "Variedad",
            "description": "Diversidad de trucos y recursos utilizados",
            "weight": 0.15
          },
          "U": {
            "name": "Uso",
            "description": "Aprovechamiento de los obstáculos y del circuito",
            "weight": 0.10
          },
          "P": {
            "name": "Penalización",
            "description": "Deducciones por fallos, caídas o interrupciones",
            "type": "penalty"
          }
        }
      }
    }
  }
}' WHERE team_sport_name = 'Skateboarding';

update "TeamSports" set team_sport_rules = '{
  "sport": "Vela",
  "disciplines": {
    "laser": {
      "scoring_rules": {
        "formula": "Pt = T + V + E + C",
        "variables": {
          "Pt": {
            "name": "Puntaje Total",
            "description": "Tiempo final ajustado de la prueba"
          },
          "T": {
            "name": "Tiempo Base",
            "description": "Tiempo registrado por el competidor en la regata",
            "unit": "seconds"
          },
          "V": {
            "name": "Variación del viento",
            "description": "Impacto de cambios de viento durante la prueba",
            "range": [0, 300],
            "unit": "seconds"
          },
          "E": {
            "name": "Errores",
            "description": "Penalización temporal por errores de navegación",
            "range": [0, 240],
            "unit": "seconds"
          },
          "C": {
            "name": "Corriente/Oleaje",
            "description": "Impacto de las condiciones marítimas",
            "range": [0, 180],
            "unit": "seconds"
          }
        }
      }
    },
    "iqfoil": {
      "scoring_rules": {
        "formula": "Pt = T + V + E + P",
        "variables": {
          "Pt": {
            "name": "Puntaje Total",
            "description": "Tiempo final ajustado de la prueba"
          },
          "T": {
            "name": "Tiempo Base",
            "description": "Tiempo registrado por el competidor",
            "unit": "seconds"
          },
          "V": {
            "name": "Variación del viento",
            "description": "Impacto de cambios de viento durante la prueba",
            "range": [0, 240],
            "unit": "seconds"
          },
          "E": {
            "name": "Errores",
            "description": "Penalizaciones temporales por fallos técnicos",
            "range": [0, 90],
            "unit": "seconds"
          },
          "P": {
            "name": "Penalizaciones",
            "description": "Sanciones reglamentarias aplicadas durante la prueba",
            "range": [0, 30],
            "unit": "seconds"
          }
        }
      }
    },
    "kite": {
      "scoring_rules": {
        "formula": "Pt = T + V + M + P",
        "variables": {
          "Pt": {
            "name": "Puntaje Total",
            "description": "Tiempo final ajustado de la prueba"
          },
          "T": {
            "name": "Tiempo Base",
            "description": "Tiempo registrado por el competidor",
            "unit": "seconds"
          },
          "V": {
            "name": "Variación del viento",
            "description": "Impacto de cambios de viento durante la prueba",
            "range": [0, 180],
            "unit": "seconds"
          },
          "M": {
            "name": "Maniobras",
            "description": "Tiempo añadido por complejidad y control de maniobras",
            "range": [0, 45],
            "unit": "seconds"
          },
          "P": {
            "name": "Penalizaciones",
            "description": "Sanciones reglamentarias aplicadas durante la prueba",
            "range": [0, 20],
            "unit": "seconds"
          }
        }
      }
    },
    "49er": {
      "scoring_rules": {
        "formula": "Pt = T + V + B + M",
        "variables": {
          "Pt": {
            "name": "Puntaje Total",
            "description": "Tiempo final ajustado de la prueba"
          },
          "T": {
            "name": "Tiempo Base",
            "description": "Tiempo registrado por la embarcación",
            "unit": "seconds"
          },
          "V": {
            "name": "Variación del viento",
            "description": "Impacto de cambios de viento durante la regata",
            "range": [0, 240],
            "unit": "seconds"
          },
          "B": {
            "name": "Balance",
            "description": "Estabilidad y equilibrio de la embarcación",
            "range": [0, 90],
            "unit": "seconds"
          },
          "M": {
            "name": "Maniobras",
            "description": "Tiempo añadido por ejecución de maniobras",
            "range": [0, 120],
            "unit": "seconds"
          }
        }
      }
    },
    "470_mixed": {
      "scoring_rules": {
        "formula": "Pt = T + V + C + A",
        "variables": {
          "Pt": {
            "name": "Puntaje Total",
            "description": "Tiempo final ajustado de la prueba"
          },
          "T": {
            "name": "Tiempo Base",
            "description": "Tiempo registrado por la embarcación",
            "unit": "seconds"
          },
          "V": {
            "name": "Variación del viento",
            "description": "Impacto de cambios de viento durante la regata",
            "range": [0, 360],
            "unit": "seconds"
          },
          "C": {
            "name": "Coordinación",
            "description": "Sincronización y trabajo conjunto de la tripulación",
            "range": [0, 180],
            "unit": "seconds"
          },
          "A": {
            "name": "Táctica",
            "description": "Capacidad estratégica y toma de decisiones",
            "range": [0, 240],
            "unit": "seconds"
          }
        }
      }
    },
    "nacra17_mixed": {
      "scoring_rules": {
        "formula": "Pt = T + V + M + P",
        "variables": {
          "Pt": {
            "name": "Puntaje Total",
            "description": "Tiempo final ajustado de la prueba"
          },
          "T": {
            "name": "Tiempo Base",
            "description": "Tiempo registrado por la embarcación",
            "unit": "seconds"
          },
          "V": {
            "name": "Variación del viento",
            "description": "Impacto de cambios de viento durante la regata",
            "range": [0, 240],
            "unit": "seconds"
          },
          "M": {
            "name": "Maniobras",
            "description": "Tiempo añadido por ejecución y complejidad de maniobras",
            "range": [0, 120],
            "unit": "seconds"
          },
          "P": {
            "name": "Penalizaciones",
            "description": "Sanciones reglamentarias aplicadas durante la prueba",
            "range": [0, 180],
            "unit": "seconds"
          }
        }
      }
    }
  }
}' WHERE team_sport_name = 'Vela';

update "TeamSports" set team_sport_rules = '{
  "sport": "Esquí Acrobático",
  "disciplines": {
    "baches": {
      "scoring_rules": {
        "formula": "(G*0.6) + (J*0.2) + (T*0.2) - P",
        "variables": {
          "G": {
            "name": "Giros",
            "description": "Calidad técnica y control en los giros",
            "weight": 0.60
          },
          "J": {
            "name": "Saltos",
            "description": "Dificultad y ejecución de los saltos",
            "weight": 0.20
          },
          "T": {
            "name": "Tiempo",
            "description": "Velocidad y tiempo total del recorrido",
            "weight": 0.20
          },
          "P": {
            "name": "Penalizaciones",
            "description": "Deducciones por errores o fallos técnicos",
            "range": [0, 15]
          }
        }
      }
    },
    "halfpipe": {
      "scoring_rules": {
        "formula": "(D*0.25) + (A*0.2) + (V*0.15) + (E*0.3) + (L*0.1) - P",
        "variables": {
          "D": {
            "name": "Dificultad",
            "description": "Complejidad técnica de la rutina",
            "weight": 0.25
          },
          "A": {
            "name": "Amplitud",
            "description": "Altura y alcance de los movimientos",
            "weight": 0.20
          },
          "V": {
            "name": "Variedad",
            "description": "Diversidad de maniobras realizadas",
            "weight": 0.15
          },
          "E": {
            "name": "Ejecución",
            "description": "Calidad y limpieza técnica de la rutina",
            "weight": 0.30
          },
          "L": {
            "name": "Landing",
            "description": "Calidad del aterrizaje",
            "weight": 0.10
          },
          "P": {
            "name": "Penalizaciones",
            "description": "Deducciones por errores o caídas",
            "range": [0, 20]
          }
        }
      }
    },
    "salto_aereo": {
      "scoring_rules": {
        "formula": "((F*0.2) + (EA*0.5) + (L*0.3) - P) * DD",
        "variables": {
          "DD": {
            "name": "Grado de dificultad",
            "description": "Coeficiente de dificultad del salto"
          },
          "F": {
            "name": "Despegue",
            "description": "Calidad y estabilidad del despegue",
            "weight": 0.20
          },
          "EA": {
            "name": "Ejecución Aérea",
            "description": "Calidad técnica durante la fase aérea",
            "weight": 0.50
          },
          "L": {
            "name": "Landing",
            "description": "Calidad y estabilidad del aterrizaje",
            "weight": 0.30
          },
          "P": {
            "name": "Penalización",
            "description": "Deducciones por errores técnicos o caídas",
            "range": [0, 30]
          }
        }
      }
    },
    "big_air": {
      "scoring_rules": {
        "formula": "(D*0.3) + (A*0.15) + (E*0.3) + (L*0.2) + (S*0.05) - P",
        "variables": {
          "D": {
            "name": "Dificultad",
            "description": "Complejidad técnica del truco",
            "weight": 0.30
          },
          "A": {
            "name": "Amplitud",
            "description": "Altura y alcance del salto",
            "weight": 0.15
          },
          "E": {
            "name": "Ejecución",
            "description": "Calidad técnica y control del truco",
            "weight": 0.30
          },
          "L": {
            "name": "Landing",
            "description": "Calidad del aterrizaje",
            "weight": 0.20
          },
          "S": {
            "name": "Estilo",
            "description": "Presentación y fluidez estética del truco",
            "weight": 0.05
          },
          "P": {
            "name": "Penalizaciones",
            "description": "Deducciones por errores o caídas",
            "range": [0, 25]
          }
        }
      }
    },
    "slopestyle": {
      "scoring_rules": {
        "formula": "(D*0.25) + (V*0.2) + (F*0.15) + (E*0.25) + (L*0.15) - P",
        "variables": {
          "D": {
            "name": "Dificultad",
            "description": "Complejidad técnica de la rutina",
            "weight": 0.25
          },
          "V": {
            "name": "Variedad",
            "description": "Diversidad de maniobras y recursos utilizados",
            "weight": 0.20
          },
          "F": {
            "name": "Fluidez",
            "description": "Continuidad y ritmo de la presentación",
            "weight": 0.15
          },
          "E": {
            "name": "Ejecución",
            "description": "Calidad técnica y limpieza de los movimientos",
            "weight": 0.25
          },
          "L": {
            "name": "Landing",
            "description": "Calidad y estabilidad del aterrizaje",
            "weight": 0.15
          },
          "P": {
            "name": "Penalizaciones",
            "description": "Deducciones por errores o caídas",
            "range": [0, 20]
          }
        }
      }
    },
    "ski_cross": {
      "scoring_rules": {
        "formula": "BT - TB + P",
        "variables": {
          "BT": {
            "name": "Tiempo Base",
            "description": "Tiempo registrado en la carrera",
            "range": [60, 70]
          },
          "TB": {
            "name": "Bonus Técnico",
            "description": "Bonificación por calidad técnica y maniobras",
            "range": [0, 5]
          },
          "P": {
            "name": "Penalizaciones",
            "description": "Tiempo añadido por infracciones o errores",
            "range": [0, 10]
          }
        }
      }
    },
    "salto_aereo_por_equipos": {
      "scoring_rules": {
        "formula": "DD * Ejecucion_Total",
        "variables": {
          "DD": {
            "name": "Grado de dificultad",
            "description": "Coeficiente de dificultad del salto grupal"
          },
          "Ejecucion_Total": {
            "name": "Ejecución Total",
            "description": "Suma de ejecuciones válidas (2 masculinas y 1 femenina)"
          }
        },
        "team_format": {
          "male_jumps_count": 2,
          "female_jumps_count": 1
        }
      }
    }
  }
}' WHERE team_sport_name = 'Esqui Acrobatico';

update "TeamSports" set team_sport_rules = '{
  "sport": "Esquí Nórdico",
  "scoring_rules": {
    "total_formula": "DP + SP + WC + GC - P",
    "distance_formula": "DP = BP + ((D - K) * MV)",
    "variables": {
      "DP": {
        "name": "Puntos de Distancia",
        "description": "Puntaje obtenido según la distancia alcanzada en el salto"
      },
      "D": {
        "name": "Distancia",
        "description": "Metros alcanzados durante el salto"
      },
      "K": {
        "name": "Valor K",
        "description": "Punto de referencia del trampolín",
        "values": {
          "normal_hill": 60,
          "large_hill": 120
        }
      },
      "SP": {
        "name": "Puntos de Estilo",
        "description": "Evaluación técnica y estética del salto",
        "range": [0, 60]
      },
      "WC": {
        "name": "Compensación por Viento",
        "description": "Ajuste por condiciones de viento",
        "range": [-20, 20]
      },
      "GC": {
        "name": "Compensación de Salida",
        "description": "Ajuste según la posición de salida",
        "range": [-10, 10]
      },
      "P": {
        "name": "Penalizaciones",
        "description": "Deducciones por errores técnicos o infracciones",
        "range": [0, 20]
      },
      "BP": {
        "name": "Puntos Base",
        "description": "Puntaje base asignado al trampolín",
        "range": [80, 160]
      },
      "MV": {
        "name": "Valor por Metro",
        "description": "Coeficiente aplicado por cada metro sobre o bajo el punto K",
        "range": [50, 100]
      }
    },
    "competition_format": {
      "individual": {
        "rounds": 2,
        "final_score": "Suma de las dos rondas"
      },
      "mixed_team": {
        "team_composition": {
          "male": 2,
          "mixed": 4
        },
        "final_score": "Suma de los puntajes de los integrantes"
      }
    }
  }
}' WHERE team_sport_name = 'Esqui Nordico';

update "TeamSports" set team_sport_rules = '{
  "sport": "Patinaje Artístico",
  "disciplines": {
    "individual": {
      "technical_element_score": {
        "formula": "TES = BV + GOE",
        "variables": {
          "BV": {
            "name": "Valor Base",
            "description": "Valor técnico base de los elementos ejecutados",
            "ranges": {
              "male": [45, 90],
              "female": [35, 70],
              "pairs": [40, 80]
            }
          },
          "GOE": {
            "name": "Grado de Ejecución",
            "description": "Evaluación de calidad técnica de los elementos",
            "range": [-10, 25]
          }
        }
      },
      "program_component_score": {
        "formula": "PCS = SS + C + I + T + S",
        "variables": {
          "SS": {
            "name": "Skating Skills",
            "description": "Calidad y dominio del patinaje",
            "range": [0, 20]
          },
          "C": {
            "name": "Coreografía",
            "description": "Diseño artístico y composición del programa",
            "range": [0, 20]
          },
          "I": {
            "name": "Interpretación",
            "description": "Expresión artística y musicalidad",
            "range": [0, 20]
          },
          "T": {
            "name": "Transiciones",
            "description": "Conexión y fluidez entre elementos",
            "range": [0, 20]
          },
          "S": {
            "name": "Sincronización",
            "description": "Coordinación general de la rutina",
            "range": [0, 20]
          }
        }
      },
      "final_score": {
        "formula": "PCS + TES - P",
        "variables": {
          "P": {
            "name": "Penalizaciones",
            "description": "Deducciones por errores o infracciones"
          }
        }
      }
    },
    "pairs_ice_dance": {
      "technical_element_score": {
        "formula": "TES = BV + GOE + L",
        "variables": {
          "BV": {
            "name": "Valor Base",
            "description": "Valor técnico base de los elementos ejecutados",
            "range": [40, 80]
          },
          "GOE": {
            "name": "Grado de Ejecución",
            "description": "Evaluación de calidad técnica",
            "range": [-10, 25]
          },
          "L": {
            "name": "Liftings",
            "description": "Calidad y dificultad de las elevaciones",
            "range": [0, 20]
          }
        }
      },
      "program_component_score": {
        "formula": "PCS = S + C + I",
        "variables": {
          "S": {
            "name": "Sincronización",
            "description": "Coordinación y armonía de la pareja",
            "range": [0, 25]
          },
          "C": {
            "name": "Coreografía",
            "description": "Diseño artístico y composición del programa",
            "range": [0, 20]
          },
          "I": {
            "name": "Interpretación",
            "description": "Expresión artística y musicalidad",
            "range": [0, 20]
          }
        }
      },
      "final_score": {
        "formula": "PCS + TES - P",
        "variables": {
          "P": {
            "name": "Penalizaciones",
            "description": "Deducciones por errores o infracciones"
          }
        }
      }
    }
  }
}' WHERE team_sport_name = 'Patinaje Artistico sobre Hielo';

update "TeamSports" set team_sport_rules = '{
  "sport": "Snowboard Acrobático",
  "disciplines": {
    "slopestyle": {
      "competition_format": {
        "rounds": 3,
        "final_score": "Mejor puntaje de las tres rondas"
      },
      "scoring_rules": {
        "formula": "(0.3*T) + (0.25*E) + (0.15*A) + (0.1*R) + (0.1*L) + (0.1*S) - P",
        "variables": {
          "T": {
            "name": "Tricks",
            "description": "Complejidad y calidad técnica de los trucos",
            "range": [40, 100],
            "weight": 0.30
          },
          "E": {
            "name": "Ejecución",
            "description": "Calidad técnica y limpieza de la rutina",
            "range": [0, 100],
            "weight": 0.25
          },
          "A": {
            "name": "Amplitud",
            "description": "Altura y alcance de los movimientos",
            "range": [0, 100],
            "weight": 0.15
          },
          "R": {
            "name": "Rieles",
            "description": "Calidad y dificultad en secciones de rieles",
            "range": [0, 100],
            "weight": 0.10
          },
          "L": {
            "name": "Landing",
            "description": "Calidad y estabilidad del aterrizaje",
            "range": [0, 100],
            "weight": 0.10
          },
          "S": {
            "name": "Estilo",
            "description": "Fluidez y presentación estética",
            "range": [0, 100],
            "weight": 0.10
          },
          "P": {
            "name": "Penalizaciones",
            "description": "Deducciones por errores o caídas",
            "range_per_penalty": [-12.5, -2.5]
          }
        }
      }
    },
    "halfpipe": {
      "competition_format": {
        "rounds": 3,
        "final_score": "Mejor puntaje de las tres rondas"
      },
      "scoring_rules": {
        "formula": "(0.28*T) + (0.25*A) + (0.2*E) + (0.1*F) + (0.1*L) + (0.07*S) - P",
        "variables": {
          "T": {
            "name": "Tricks",
            "description": "Complejidad y calidad técnica de los trucos",
            "range": [40, 100],
            "weight": 0.28
          },
          "A": {
            "name": "Amplitud",
            "description": "Altura y alcance de los movimientos",
            "range": [0, 100],
            "weight": 0.25
          },
          "E": {
            "name": "Ejecución",
            "description": "Calidad técnica y control de la rutina",
            "range": [0, 100],
            "weight": 0.20
          },
          "F": {
            "name": "Flow",
            "description": "Fluidez y continuidad de la presentación",
            "range": [0, 100],
            "weight": 0.10
          },
          "L": {
            "name": "Landing",
            "description": "Calidad y estabilidad del aterrizaje",
            "range": [0, 100],
            "weight": 0.10
          },
          "S": {
            "name": "Estilo",
            "description": "Presentación estética y creatividad",
            "range": [0, 100],
            "weight": 0.07
          },
          "P": {
            "name": "Penalizaciones",
            "description": "Deducciones por errores o caídas",
            "range_per_penalty": [-12.5, -2.5]
          }
        }
      }
    },
    "big_air": {
      "competition_format": {
        "rounds": 3,
        "final_score": "Suma de las dos mejores rondas"
      },
      "scoring_rules": {
        "formula": "(0.35*T) + (0.15*A) + (0.25*E) + (0.05*G) + (0.15*L) + (0.05*S) - P",
        "variables": {
          "T": {
            "name": "Tricks",
            "description": "Complejidad y calidad técnica de los trucos",
            "range": [40, 100],
            "weight": 0.35
          },
          "A": {
            "name": "Amplitud",
            "description": "Altura y alcance del salto",
            "range": [0, 100],
            "weight": 0.15
          },
          "E": {
            "name": "Ejecución",
            "description": "Calidad técnica y control de la maniobra",
            "range": [0, 100],
            "weight": 0.25
          },
          "G": {
            "name": "Grab",
            "description": "Calidad y dificultad del grab realizado",
            "range": [0, 100],
            "weight": 0.05
          },
          "L": {
            "name": "Landing",
            "description": "Calidad y estabilidad del aterrizaje",
            "range": [0, 100],
            "weight": 0.15
          },
          "S": {
            "name": "Estilo",
            "description": "Presentación estética y creatividad",
            "range": [0, 100],
            "weight": 0.05
          },
          "P": {
            "name": "Penalizaciones",
            "description": "Deducciones por errores o caídas",
            "range_per_penalty": [-12.5, -2.5]
          }
        }
      }
    }
  }
}' WHERE team_sport_name = 'Snowboard Acrobatico';

update "TeamSports" set team_sport_rules = '{
  "sport": "Ciclismo Urbano",
  "scoring_rules": {
    "formula": "(0.3*D) + (0.25*E) + (0.2*A) + (0.15*F) + (0.1*C) + R - P",
    "variables": {
      "D": {
        "name": "Dificultad",
        "description": "Complejidad técnica de los trucos y maniobras",
        "weight": 0.30
      },
      "E": {
        "name": "Ejecución",
        "description": "Calidad y limpieza de la ejecución",
        "weight": 0.25
      },
      "A": {
        "name": "Amplitud",
        "description": "Altura, alcance o magnitud de los movimientos",
        "weight": 0.20
      },
      "F": {
        "name": "Flow",
        "description": "Fluidez y continuidad de la rutina",
        "weight": 0.15
      },
      "C": {
        "name": "Creatividad",
        "description": "Originalidad y variedad de la presentación",
        "weight": 0.10
      },
      "R": {
        "name": "Random",
        "description": "Factor aleatorio adicional para variabilidad de simulación",
        "type": "bonus"
      },
      "P": {
        "name": "Penalización",
        "description": "Deducciones por errores, caídas o infracciones",
        "type": "penalty",
        "possible_values": [-5, -10, -20, -40]
      }
    }
  }
}' WHERE team_sport_name = 'Ciclismo Urbano';


select * from "TeamSports";
