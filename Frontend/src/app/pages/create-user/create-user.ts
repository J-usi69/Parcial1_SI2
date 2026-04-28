import { Component } from '@angular/core';
import { NewUserForm } from '../../components/new-user-form/new-user-form';

@Component({
  selector: 'app-create-user',
  imports: [NewUserForm],
  templateUrl: './create-user.html',
  styleUrl: './create-user.css',
  standalone: true,
})
export class CreateUser {}
