import { Component } from '@angular/core';
import {
  NewRequestCard,
  NewRequestData,
} from '../../../components/new-request-card/new-request-card';

@Component({
  selector: 'app-new-requests',
  imports: [NewRequestCard],
  templateUrl: './new-requests.html',
  styleUrl: './new-requests.css',
})
export class NewRequests {
  requests: NewRequestData[] = [
    {
      titulo: 'Fallo de Batería',
      tiempo: '2 mins',
      severidad: 'Crítico',
      vehiculo: 'Toyota Hilux',
      placa: 'ABC-123',
      ubicacion: 'Av. Javier Prado Este',
      distancia: '4.2 km',
    },
    {
      titulo: 'Overheating',
      tiempo: '5 mins',
      severidad: 'Alto',
      vehiculo: 'BMW X5',
      placa: 'XYZ-789',
      ubicacion: 'Panamericana Sur',
      distancia: '12 km',
    },
    {
      titulo: 'Neumático Desinflado',
      tiempo: '8 mins',
      severidad: 'Medio',
      vehiculo: 'Kia Carnival',
      placa: 'LMN-456',
      ubicacion: 'Miraflores',
      distancia: '2.1 km',
    },
  ];
}
