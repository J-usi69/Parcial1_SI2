import { Component, Input } from '@angular/core';
import { ButtonComponent } from '../button/button';

@Component({
  selector: 'app-sucursal-card', // Nombre del selector para usarlo
  standalone: true,
  imports: [ButtonComponent],
  templateUrl: './sucursal-card.html',
})
export class SucursalCard {
  // Aquí defines las entradas de datos con valores por defecto
  @Input() titulo: string = 'Nombre de Sucursal';
  @Input() direccion: string = 'Dirección no disponible';
  @Input() tecnicos: number | string = 0;
  @Input() vehiculos: number | string = 0;
  @Input() contacto: string = '';
  @Input() urlDetalle: string = '/home';
  @Input() badgeText: string = 'Sucursal';
}
