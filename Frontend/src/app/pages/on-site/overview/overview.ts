import { Component } from '@angular/core';
import { MapComponent } from '../../../components/map/map';
import { CardData, RequestCardComponent } from '../../../components/request-card/request-card';

@Component({
  selector: 'app-overview',
  imports: [MapComponent, RequestCardComponent],
  templateUrl: './overview.html',
  styleUrl: './overview.css',
})
export class Overview {
  marcadores = [
    {
      position: { lat: -17.7833, lng: -63.1821 },
      titulo: 'Santa Cruz',
    },
  ];
  miSolicitud: CardData[] = [
    {
      tipo: 'Motor',
      titulo: 'Audi A4',
      tiempo: 'Hace 10 min',
      usuario: 'Elena Rodríguez',
      ubicacion: 'Av. de la Castellana 15, Madrid',
    },
    {
      tipo: 'Motor',
      titulo: 'Audi A4',
      tiempo: 'Hace 10 min',
      usuario: 'Elena Rz',
      ubicacion: 'Av. de la Castel15, Madrid',
    },
  ];
}
