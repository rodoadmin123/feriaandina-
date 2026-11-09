import { useEffect, useState } from "react";
import Icono from "../../../compartido/componentes/Icono.jsx";

// capture="environment" abre DIRECTO la camara trasera del celular:
// el artesano toma la foto en el puesto del mercado, sin buscar archivos.
export default function SelectorFoto({ foto, onElegir }) {
  const [vista, setVista] = useState(null);

  useEffect(() => {
    if (!foto) { setVista(null); return; }
    const url = URL.createObjectURL(foto);   // vista previa local
    setVista(url);
    return () => URL.revokeObjectURL(url);
  }, [foto]);

  return (
    <label className={`selector-foto ${vista ? "con-foto" : ""}`}>
      <input type="file" accept="image/*" capture="environment" data-testid="foto"
        onChange={(e) => onElegir(e.target.files[0] || null)} />
      {vista ? (
        <>
          <img src={vista} alt="Vista previa del producto" />
          <span className="cambiar-foto">Cambiar foto</span>
        </>
      ) : (
        <span className="selector-vacio">
          <span className="circulo-camara"><Icono nombre="camara" tam={34} /></span>
          <strong>Toma una foto</strong>
          <small>Toca aquí y se abre la cámara</small>
        </span>
      )}
    </label>
  );
}
