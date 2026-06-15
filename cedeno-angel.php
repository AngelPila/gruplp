<?php

$resultado = null;
$encontrado = false;
$precio = 100.0;
$descuento = 4.0;
$precio_final = $precio / $descuento;   
$dividendo = 256.0;
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
 
$activo = false;
if ($activo != true) {
    $resultado = evaluar($precio_final, 30.5);
}
 
echo "Precio final: " . $precio_final;
echo "Dividendo: " . $dividendo;
echo "Resultado: " . $resultado;
 
?>