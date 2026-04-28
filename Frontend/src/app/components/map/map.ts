import { Component, Input, CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';
import { GoogleMapsModule } from '@angular/google-maps';

import { Marcador } from '../../interfaces/marcador.interface';

@Component({
  selector: 'app-map',
  standalone: true,
  //funciona pero no se porque esta en rojo
  imports: [GoogleMapsModule],
  schemas: [CUSTOM_ELEMENTS_SCHEMA],
  template: `
    <google-map height="400px" width="100%" [center]="center" [zoom]="zoom">
      @for (m of marcadores; track m.titulo) {
        <map-marker [position]="m.position" [title]="m.titulo"></map-marker>
      }
    </google-map>
  `,
})
export class MapComponent {
  @Input() marcadores: Marcador[] = [];
  center = { lat: -17.7833, lng: -63.1821 }; // Santa Cruz
  zoom = 13;
}
