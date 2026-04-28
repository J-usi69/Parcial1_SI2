import { Component } from '@angular/core';
import { ButtonComponent } from '../button/button';

@Component({
  standalone: true,
  selector: 'app-new-branch-form',
  imports: [ButtonComponent],
  templateUrl: './new-branch-form.html',
  styleUrl: './new-branch-form.css',
})
export class NewBranchForm {}
