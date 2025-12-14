import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { CdkDragDrop, moveItemInArray, transferArrayItem, DragDropModule } from '@angular/cdk/drag-drop';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatDialog, MatDialogModule } from '@angular/material/dialog';
import { MatChipsModule } from '@angular/material/chips';
import { ConferenceService } from '../conference.service';
import { Conference, ConferenceStatus, ConferenceLevel } from '../../../models/conference';
import { ConferenceDialogComponent } from '../conference-dialog/conference-dialog.component';

@Component({
  selector: 'app-kanban-board',
  standalone: true,
  imports: [
    CommonModule,
    DragDropModule,
    MatCardModule,
    MatButtonModule,
    MatIconModule,
    MatChipsModule,
    MatDialogModule
  ],
  templateUrl: './kanban-board.component.html',
  styleUrl: './kanban-board.component.css'
})
export class KanbanBoardComponent implements OnInit {
  // Fixed columns as per requirement
  columns = Object.values(ConferenceStatus);

  // Level mapping for display
  levelLabels: { [key in ConferenceLevel]: string } = {
    [ConferenceLevel.EASY]: 'Facile',
    [ConferenceLevel.MID]: 'Moyen',
    [ConferenceLevel.EXPERT]: 'Expert'
  };

  // Data structure: Map status to list of conferences
  boardData: { [key: string]: Conference[] } = {};

  constructor(
    private conferenceService: ConferenceService,
    private dialog: MatDialog
  ) {
    // Initialize empty lists for each status
    this.columns.forEach(col => this.boardData[col] = []);
  }

  ngOnInit(): void {
    this.loadConferences();
  }

  loadConferences() {
    this.conferenceService.getConferences().subscribe(data => {
      // Reset board
      this.columns.forEach(col => this.boardData[col] = []);

      // Distribute conferences
      data.forEach(conf => {
        if (this.boardData[conf.status]) {
          this.boardData[conf.status].push(conf);
        } else {
          // Fallback for unknown status, maybe put in first column or log
          console.warn('Unknown status:', conf.status);
        }
      });
    });
  }

  drop(event: CdkDragDrop<Conference[]>) {
    if (event.previousContainer === event.container) {
      moveItemInArray(event.container.data, event.previousIndex, event.currentIndex);
    } else {
      const conference = event.previousContainer.data[event.previousIndex];
      const newStatus = event.container.id as ConferenceStatus;

      transferArrayItem(
        event.previousContainer.data,
        event.container.data,
        event.previousIndex,
        event.currentIndex,
      );

      // Update backend
      this.conferenceService.updateConference(conference.id!, { status: newStatus }).subscribe({
        next: (updated) => {
          // Update local object if needed, or rely on transferArrayItem
          conference.status = newStatus;
        },
        error: (err) => {
          console.error('Failed to update status', err);
          // Revert move on error? For prototype, just logging.
          // To revert: transfer back.
        }
      });
    }
  }

  getConnectedList(): string[] {
    return this.columns;
  }

  openDialog(conference?: Conference): void {
    const dialogRef = this.dialog.open(ConferenceDialogComponent, {
      width: '600px',
      data: conference ? { ...conference } : null
    });

    dialogRef.afterClosed().subscribe(result => {
      if (result) {
        if (conference && conference.id) {
          // Update
          this.conferenceService.updateConference(conference.id, result).subscribe(() => this.loadConferences());
        } else {
          // Create
          this.conferenceService.createConference(result).subscribe(() => this.loadConferences());
        }
      }
    });
  }
}
