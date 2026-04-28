import { Component, Input, Output, EventEmitter } from '@angular/core';
import { RouterModule } from '@angular/router';

@Component({
  selector: 'app-button',
  standalone: true,
  imports: [RouterModule],
  templateUrl: './button.html',
  styleUrls: ['./button.css'],
})
export class ButtonComponent {
  @Input() label: string = 'Botón';
  @Input() url: string = '/';

  // Creamos un evento personalizado que el padre podrá escuchar
  @Output() onClick = new EventEmitter<void>();

  ejecutarAccion() {
    this.onClick.emit(); // Avisa al padre que se hizo clic
  }
}
