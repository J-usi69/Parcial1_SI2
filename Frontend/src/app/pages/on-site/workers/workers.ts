import { Component } from '@angular/core';
import { ButtonComponent } from '../../../components/button/button';
import { WorkerCard, WorkerData } from '../../../components/worker-card/worker-card';

@Component({
  selector: 'app-workers',
  imports: [ButtonComponent, WorkerCard],
  templateUrl: './workers.html',
  styleUrl: './workers.css',
})
export class Workers {
  // Aquí defines tu "N" cantidad de trabajadores
  listaTrabajadores: WorkerData[] = [
    {
      nombre: 'Carlos Mendoza',
      especialidad: 'Diagnóstico Eléctrico',
      isOnline: true,
      fotoUrl:
        'https://lh3.googleusercontent.com/aida-public/AB6AXuC2YTSw_viLu7bDaKmVhLhtsuycHce8394w9Elpz5DbqUW90MtO2UhidpiJ97W1GmYMDxqzstotD-oEn_Et_2mTxtHO6ycy3P7ywhj-9_P7TdikaGlHIopT8kSpN0lV1i_3p4D5mX02VadvrV5ozSq-tpQF4Nqkd8NT3uQebqDAvzTIL7RfGszMXdHZGrDaMJiDXkJu1MCU4ZWQHg4JlDZpnYF2iEG04Rg3t-y5xhgtS1y1Rrj16YYHoNxCsOZ9mP_SZ5sXuPI4mzY',
    },
    {
      nombre: 'Ana López',
      especialidad: 'Mecánica General',
      isOnline: false,
      fotoUrl: 'http://googleusercontent.com/profile/picture/1',
    },
    {
      nombre: 'Luis Pérez',
      especialidad: 'Sistemas de Inyección',
      isOnline: true,
      fotoUrl: 'http://googleusercontent.com/profile/picture/2',
    },
    // Puedes agregar tantos como necesites aquí
  ];
}
