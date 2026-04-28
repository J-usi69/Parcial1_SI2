import { Component } from '@angular/core';
import { ButtonComponent } from '../../../components/button/button';
import { SucursalCard } from '../../../components/sucursal-card/sucursal-card';

@Component({
  selector: 'app-administracion',
  standalone: true,
  imports: [ButtonComponent, SucursalCard],
  templateUrl: './administracion.html',
  styleUrl: './administracion.css',
})
export class Administracion {
  // Esta lista representa tu "n" cantidad de registros
  sucursales = [
    {
      badgeText: 'Sede Central',
      titulo: 'Sucursal Norte - Madrid',
      direccion: 'Av. de la Innovación 45, Madrid',
      tecnicos: 24,
      vehiculos: 18,
      contacto: '+34 912 345 678',
      urlDetalle: '/detalle-sucursal',
    },
    {
      badgeText: 'Sucursal',
      titulo: 'Sucursal Sur - Sevilla',
      direccion: 'Calle del Sol 12, Sevilla',
      tecnicos: 12,
      vehiculos: 8,
      contacto: '+34 954 123 456',
      urlDetalle: '/detalle-sucursal',
    },
  ];
}
