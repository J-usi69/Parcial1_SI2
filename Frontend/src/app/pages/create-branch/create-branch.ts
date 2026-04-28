import { Component } from '@angular/core';
import { NewBranchForm } from '../../components/new-branch-form/new-branch-form';
@Component({
  selector: 'app-create-branch',
  imports: [NewBranchForm],
  templateUrl: './create-branch.html',
  styleUrl: './create-branch.css',
})
export class CreateBranch {}
