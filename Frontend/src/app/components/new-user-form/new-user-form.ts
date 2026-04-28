import { Component } from '@angular/core';
import { ButtonComponent } from '../button/button';

@Component({
  selector: 'app-new-user-form',
  imports: [ButtonComponent],
  templateUrl: './new-user-form.html',
  styleUrl: './new-user-form.css',
  standalone: true,
})
export class NewUserForm {}
