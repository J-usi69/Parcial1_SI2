import { Component, Input } from '@angular/core';
import { ButtonComponent } from '../button/button';

// Interfaz para tipar los datos que recibirá el componente
export interface CardData {
  tipo: string;
  titulo: string;
  tiempo: string;
  usuario: string;
  ubicacion: string;
}

@Component({
  selector: 'app-request-card',
  standalone: true,
  templateUrl: './request-card.html',
  imports: [ButtonComponent],
})
export class RequestCardComponent {
  // @Input() permite recibir los datos desde el padre
  @Input({ required: true }) data!: CardData;
}
