import { Component } from '@angular/core';
import { ButtonComponent } from '../../../components/button/button';
import { VehicleCard, VehicleData } from '../../../components/vehicle-card/vehicle-card';

@Component({
  selector: 'app-vehicles',
  standalone: true, // Asegúrate de incluir esto
  imports: [ButtonComponent, VehicleCard],
  templateUrl: './vehicles.html',
  styleUrl: './vehicles.css',
})
export class Vehicles {
  listaVehiculos: VehicleData[] = [
    {
      nombre: 'Ford F-150 Heavy Duty',
      placa: 'VLT-7892',
      sector: 'Sector Norte',
      estado: 'ONLINE',
      imagen: 'https://images.unsplash.com/photo-1599307369324-5d5543c7b271?q=80&w=600',
      asignado: 'Juan Perez',
    },
    {
      nombre: 'Chevrolet Silverado',
      placa: 'VLT-4421',
      sector: 'Zona Industrial',
      estado: 'ONLINE',
      imagen: 'https://images.unsplash.com/photo-1551830820-2508e8b6136d?q=80&w=600',
      asignado: 'Juan Perez',
    },
    {
      nombre: 'Chevrolet Silverado',
      placa: 'VLT-4421',
      sector: 'Zona Industrial',
      estado: 'ONLINE',
      imagen: 'https://images.unsplash.com/photo-1551830820-2508e8b6136d?q=80&w=600',
      asignado: 'Juan Perez',
    },
    {
      nombre: 'Chevrolet Silverado',
      placa: 'VLT-4421',
      sector: 'Zona Industrial',
      estado: 'ONLINE',
      imagen: 'https://images.unsplash.com/photo-1551830820-2508e8b6136d?q=80&w=600',
      asignado: 'Juan Perez',
    },
    {
      nombre: 'Chevrolet Silverado',
      placa: 'VLT-4421',
      sector: 'Zona Industrial',
      estado: 'ONLINE',
      imagen: 'https://images.unsplash.com/photo-1551830820-2508e8b6136d?q=80&w=600',
      asignado: 'Juan Perez',
    },
  ];
}
