// CONTEXTO ARTESANOS
import { pedirApi } from "../../compartido/api.js";

export const listarArtesanos = () => pedirApi("/artesanos/");
