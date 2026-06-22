<?php

$resultado = null;
$encontrado = false;
$precio = 100.0;
$descuento = 4.0;
$precio_final = $precio / $descuento;
$dividendo = 256.0;

$categorias = ["bajo", "medio", "alto"];
$historial = [];

echo "Ingrese el limite de comparacion: ";
$limite_input = fgets(STDIN, 100);

while ($dividendo >= 2.0) {
    $dividendo /= 2.0;
}

function evaluar($valor, $limite) {
    if ($valor != 0) {
        if ($valor >= $limite) {
            return "alto";
        }
        return "bajo";
    }
    return null;
}

function clasificar($precio, $categorias) {
    $nivel = null;
    for ($i = 0; $i < 3; $i++) {
        if ($precio >= 50.0) {
            $nivel = $categorias[2];
        } elseif ($precio >= 25.0) {
            $nivel = $categorias[1];
        } else {
            $nivel = $categorias[0];
        }
    }
    return $nivel;
}

$activo = false;
if ($activo != true) {
    $resultado = evaluar($precio_final, 30.5);
}

$historial[] = $precio_final;
$historial[] = $dividendo;
$historial[0] = $precio_final * 2.0;

switch ($resultado) {
    case "alto":
        echo "Clasificacion: precio elevado";
        break;
    case "bajo":
        echo "Clasificacion: precio accesible";
        break;
    default:
        echo "Clasificacion: sin datos";
        break;
}

echo "Precio final: " . $precio_final;
echo "Dividendo: " . $dividendo;
echo "Resultado: " . $resultado;
echo "Categoria: " . clasificar($precio_final, $categorias);
echo "Historial 0: " . $historial[0];

?>