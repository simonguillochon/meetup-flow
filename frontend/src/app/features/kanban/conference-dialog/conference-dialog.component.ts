import { Component, Inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormBuilder, FormGroup, Validators } from '@angular/forms';
import { MatDialogRef, MAT_DIALOG_DATA, MatDialogModule } from '@angular/material/dialog';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatSelectModule } from '@angular/material/select';
import { MatDatepickerModule } from '@angular/material/datepicker';
import { MatNativeDateModule } from '@angular/material/core';
import { MatButtonModule } from '@angular/material/button';
import { Conference, ConferenceStatus, ConferenceLevel } from '../../../models/conference';

@Component({
  selector: 'app-conference-dialog',
  standalone: true,
  imports: [
    CommonModule,
    ReactiveFormsModule,
    MatDialogModule,
    MatFormFieldModule,
    MatInputModule,
    MatSelectModule,
    MatDatepickerModule,
    MatNativeDateModule,
    MatButtonModule
  ],
  templateUrl: './conference-dialog.component.html',
  styleUrl: './conference-dialog.component.css'
})
export class ConferenceDialogComponent {
  form: FormGroup;
  statusOptions = Object.values(ConferenceStatus);
  levelOptions = Object.values(ConferenceLevel);

  // Level mapping for display
  levelLabels: { [key in ConferenceLevel]: string } = {
    [ConferenceLevel.EASY]: 'Facile',
    [ConferenceLevel.MID]: 'Moyen',
    [ConferenceLevel.EXPERT]: 'Expert'
  };

  constructor(
    private fb: FormBuilder,
    public dialogRef: MatDialogRef<ConferenceDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: Conference | null
  ) {
    this.form = this.fb.group({
      title: [data?.title || '', Validators.required],
      status: [data?.status || ConferenceStatus.IDEES, Validators.required],
      assignee: [data?.assignee || ''],
      date: [data?.date ? new Date(data.date) : null],
      link_doc: [data?.link_doc || ''],
      address: [data?.address || ''],
      level: [data?.level || ConferenceLevel.EASY]
    });
  }

  onCancel(): void {
    this.dialogRef.close();
  }

  onSave(): void {
    if (this.form.valid) {
      const formValue = this.form.value;
      // Convert date to ISO string if present
      if (formValue.date) {
        formValue.date = new Date(formValue.date).toISOString();
      }
      this.dialogRef.close(formValue);
    }
  }
}
