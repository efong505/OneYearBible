# Angular One Year Bible - Step-by-Step Tutorial

## Prerequisites
- Node.js (v18+)
- Angular CLI
- Git

## Step 1: Setup Angular Project

```bash
# Install Angular CLI
npm install -g @angular/cli

# Create new Angular project
ng new one-year-bible-angular --routing --style=scss
cd one-year-bible-angular

# Install Bootstrap
npm install bootstrap
```

## Step 2: Configure Bootstrap

**angular.json**
```json
"styles": [
  "node_modules/bootstrap/dist/css/bootstrap.min.css",
  "src/styles.scss"
],
"scripts": [
  "node_modules/bootstrap/dist/js/bootstrap.bundle.min.js"
]
```

## Step 3: Create Models

**src/app/models/reading.model.ts**
```typescript
export interface Reading {
  date: string;
  dayOfWeek: string;
  title: string;
  audioUrl?: string;
  oldTestament: Scripture[];
  newTestament: Scripture[];
}

export interface Scripture {
  book: string;
  chapter?: string;
  verses: Verse[];
}

export interface Verse {
  number: number;
  text: string;
}
```

## Step 4: Create Services

**src/app/services/reading.service.ts**
```typescript
import { Injectable } from '@angular/core';
import { Observable, of } from 'rxjs';
import { Reading } from '../models/reading.model';

@Injectable({
  providedIn: 'root'
})
export class ReadingService {
  private availableReadings = ['0918', '0919', '0920', '0921', '0922', '0923'];

  getAvailableReadings(): string[] {
    return this.availableReadings;
  }

  getReading(dateCode: string): Observable<Reading | null> {
    if (this.availableReadings.includes(dateCode)) {
      return of(this.mockReading(dateCode));
    }
    return of(null);
  }

  private mockReading(dateCode: string): Reading {
    return {
      date: `September ${dateCode.slice(2)}`,
      dayOfWeek: 'Monday',
      title: 'Sample Reading',
      oldTestament: [],
      newTestament: []
    };
  }
}
```

**src/app/services/calendar.service.ts**
```typescript
import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class CalendarService {
  private currentDate = new BehaviorSubject<Date>(new Date());
  currentDate$ = this.currentDate.asObservable();

  private months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];

  setCurrentDate(date: Date): void {
    this.currentDate.next(date);
  }

  getMonthName(monthIndex: number): string {
    return this.months[monthIndex];
  }

  generateCalendarDays(year: number, month: number): any[] {
    const firstDay = new Date(year, month, 1).getDay();
    const lastDate = new Date(year, month + 1, 0).getDate();
    const prevLastDate = new Date(year, month, 0).getDate();
    
    const days = [];
    
    // Previous month days
    for (let i = firstDay; i > 0; i--) {
      days.push({ day: prevLastDate - i + 1, inactive: true });
    }
    
    // Current month days
    for (let i = 1; i <= lastDate; i++) {
      const isToday = this.isToday(year, month, i);
      days.push({ day: i, inactive: false, isToday });
    }
    
    return days;
  }

  private isToday(year: number, month: number, day: number): boolean {
    const today = new Date();
    return day === today.getDate() && 
           month === today.getMonth() && 
           year === today.getFullYear();
  }
}
```

## Step 5: Create Calendar Component

```bash
ng generate component components/calendar-widget
```

**src/app/components/calendar-widget/calendar-widget.component.ts**
```typescript
import { Component, Input, Output, EventEmitter, OnInit } from '@angular/core';
import { CalendarService } from '../../services/calendar.service';
import { ReadingService } from '../../services/reading.service';

@Component({
  selector: 'app-calendar-widget',
  templateUrl: './calendar-widget.component.html',
  styleUrls: ['./calendar-widget.component.scss']
})
export class CalendarWidgetComponent implements OnInit {
  @Input() currentPageDate?: string;
  @Output() dateSelected = new EventEmitter<string>();

  currentYear = new Date().getFullYear();
  currentMonth = new Date().getMonth();
  calendarDays: any[] = [];
  availableReadings: string[] = [];

  constructor(
    private calendarService: CalendarService,
    private readingService: ReadingService
  ) {}

  ngOnInit(): void {
    this.availableReadings = this.readingService.getAvailableReadings();
    this.generateCalendar();
  }

  generateCalendar(): void {
    this.calendarDays = this.calendarService.generateCalendarDays(this.currentYear, this.currentMonth);
  }

  getMonthName(): string {
    return this.calendarService.getMonthName(this.currentMonth);
  }

  onDateClick(day: any): void {
    if (day.inactive) return;
    
    const monthStr = (this.currentMonth + 1).toString().padStart(2, '0');
    const dayStr = day.day.toString().padStart(2, '0');
    const dateCode = monthStr + dayStr;
    
    this.dateSelected.emit(dateCode);
  }

  previousMonth(): void {
    this.currentMonth--;
    if (this.currentMonth < 0) {
      this.currentMonth = 11;
      this.currentYear--;
    }
    this.generateCalendar();
  }

  nextMonth(): void {
    this.currentMonth++;
    if (this.currentMonth > 11) {
      this.currentMonth = 0;
      this.currentYear++;
    }
    this.generateCalendar();
  }

  isAvailable(day: any): boolean {
    if (day.inactive) return false;
    const monthStr = (this.currentMonth + 1).toString().padStart(2, '0');
    const dayStr = day.day.toString().padStart(2, '0');
    const dateCode = monthStr + dayStr;
    return this.availableReadings.includes(dateCode);
  }

  isCurrentPage(day: any): boolean {
    if (!this.currentPageDate || day.inactive) return false;
    const monthStr = (this.currentMonth + 1).toString().padStart(2, '0');
    const dayStr = day.day.toString().padStart(2, '0');
    const dateCode = monthStr + dayStr;
    return dateCode === this.currentPageDate;
  }
}
```

**src/app/components/calendar-widget/calendar-widget.component.html**
```html
<div class="calendar-widget-inline">
  <div class="widget-header">
    <span class="widget-current-date">{{ getMonthName() }} {{ currentYear }}</span>
    <div class="widget-navigation">
      <span class="material-symbols-rounded" (click)="previousMonth()">chevron_left</span>
      <span class="material-symbols-rounded" (click)="nextMonth()">chevron_right</span>
    </div>
  </div>
  <div class="widget-body">
    <ul class="widget-weekdays">
      <li>S</li><li>M</li><li>T</li><li>W</li><li>T</li><li>F</li><li>S</li>
    </ul>
    <ul class="widget-dates">
      <li *ngFor="let day of calendarDays" 
          [class.inactive]="day.inactive"
          [class.active]="day.isToday || isCurrentPage(day)"
          [class.available]="isAvailable(day)"
          (click)="onDateClick(day)">
        {{ day.day }}
      </li>
    </ul>
  </div>
</div>
```

## Step 6: Create Pages

```bash
ng generate component pages/home
ng generate component pages/reading
ng generate component pages/coming-soon
```

**src/app/pages/home/home.component.ts**
```typescript
import { Component } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent {
  constructor(private router: Router) {}

  onDateSelected(dateCode: string): void {
    this.router.navigate(['/reading', dateCode]);
  }

  goToToday(): void {
    const today = new Date();
    const monthStr = (today.getMonth() + 1).toString().padStart(2, '0');
    const dayStr = today.getDate().toString().padStart(2, '0');
    const dateCode = monthStr + dayStr;
    this.router.navigate(['/reading', dateCode]);
  }
}
```

**src/app/pages/reading/reading.component.ts**
```typescript
import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { ReadingService } from '../../services/reading.service';
import { Reading } from '../../models/reading.model';

@Component({
  selector: 'app-reading',
  templateUrl: './reading.component.html',
  styleUrls: ['./reading.component.scss']
})
export class ReadingComponent implements OnInit {
  reading?: Reading;
  dateCode?: string;
  loading = true;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private readingService: ReadingService
  ) {}

  ngOnInit(): void {
    this.route.params.subscribe(params => {
      this.dateCode = params['date'];
      this.loadReading();
    });
  }

  loadReading(): void {
    if (!this.dateCode) return;
    
    this.readingService.getReading(this.dateCode).subscribe(reading => {
      if (reading) {
        this.reading = reading;
      } else {
        this.router.navigate(['/coming-soon'], { queryParams: { date: this.dateCode } });
      }
      this.loading = false;
    });
  }

  onDateSelected(dateCode: string): void {
    this.router.navigate(['/reading', dateCode]);
  }

  previousDay(): void {
    // Implementation for previous day navigation
  }

  nextDay(): void {
    // Implementation for next day navigation
  }
}
```

## Step 7: Setup Routing

**src/app/app-routing.module.ts**
```typescript
import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { HomeComponent } from './pages/home/home.component';
import { ReadingComponent } from './pages/reading/reading.component';
import { ComingSoonComponent } from './pages/coming-soon/coming-soon.component';

const routes: Routes = [
  { path: '', component: HomeComponent },
  { path: 'reading/:date', component: ReadingComponent },
  { path: 'coming-soon', component: ComingSoonComponent },
  { path: '**', redirectTo: '' }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
```

## Step 8: Copy Styles

Copy your existing CSS files to `src/assets/styles/` and import them in `src/styles.scss`:

```scss
@import 'assets/styles/widget-style.css';
@import 'assets/styles/scripture-style.css';
```

## Step 9: Add Material Icons

**src/index.html**
```html
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600" rel="stylesheet">
```

## Step 10: Build and Test

```bash
# Development server
ng serve

# Production build
ng build --prod
```

## Step 11: Data Migration

Create JSON files in `src/assets/data/` for your scripture content:

**src/assets/data/readings/0922.json**
```json
{
  "date": "September 22",
  "dayOfWeek": "Monday",
  "title": "Song of Solomon 6:11 - Isaiah 1:31",
  "audioUrl": "https://d24muyyuu3zj8g.cloudfront.net/2025/september/4/sept22.mp3",
  "oldTestament": [
    {
      "book": "Song of Solomon",
      "chapter": "6:11-13",
      "verses": [
        { "number": 11, "text": "I went down into the garden of nuts..." }
      ]
    }
  ]
}
```

This creates a modern, maintainable Angular application with the same functionality as your current project, ready for AWS deployment.

---




# Administrative Backend with Lambda Functions

## Architecture Overview

```
Frontend (Angular) → API Gateway → Lambda Functions → DynamoDB
                                                   ↓
                                              S3 (Audio Files)
```

## Step 1: AWS Backend Infrastructure

### DynamoDB Table Structure
```json
{
  "TableName": "BibleReadings",
  "KeySchema": [
    { "AttributeName": "dateCode", "KeyType": "HASH" }
  ],
  "AttributeDefinitions": [
    { "AttributeName": "dateCode", "AttributeType": "S" }
  ]
}
```

### Sample DynamoDB Record
```json
{
  "dateCode": "0922",
  "date": "September 22",
  "dayOfWeek": "Monday",
  "title": "Song of Solomon 6:11 - Isaiah 1:31",
  "audioUrl": "https://s3.amazonaws.com/bucket/sept22.mp3",
  "oldTestament": [
    {
      "book": "Song of Solomon",
      "chapter": "6:11-13",
      "verses": [
        { "number": 11, "text": "I went down into the garden..." }
      ]
    }
  ],
  "newTestament": [],
  "createdAt": "2024-01-01T00:00:00Z",
  "updatedAt": "2024-01-01T00:00:00Z"
}
```

## Step 2: Lambda Functions

### Reading CRUD Lambda (Node.js)
```javascript
// lambda/readings-crud.js
const AWS = require('aws-sdk');
const dynamodb = new AWS.DynamoDB.DocumentClient();

exports.handler = async (event) => {
  const { httpMethod, pathParameters, body } = event;
  const dateCode = pathParameters?.dateCode;
  
  try {
    switch (httpMethod) {
      case 'GET':
        return await getReading(dateCode);
      case 'POST':
        return await createReading(JSON.parse(body));
      case 'PUT':
        return await updateReading(dateCode, JSON.parse(body));
      case 'DELETE':
        return await deleteReading(dateCode);
      default:
        return { statusCode: 405, body: 'Method Not Allowed' };
    }
  } catch (error) {
    return { statusCode: 500, body: JSON.stringify({ error: error.message }) };
  }
};

async function getReading(dateCode) {
  if (dateCode) {
    const result = await dynamodb.get({
      TableName: 'BibleReadings',
      Key: { dateCode }
    }).promise();
    return { statusCode: 200, body: JSON.stringify(result.Item) };
  } else {
    const result = await dynamodb.scan({ TableName: 'BibleReadings' }).promise();
    return { statusCode: 200, body: JSON.stringify(result.Items) };
  }
}

async function createReading(reading) {
  reading.createdAt = new Date().toISOString();
  reading.updatedAt = new Date().toISOString();
  
  await dynamodb.put({
    TableName: 'BibleReadings',
    Item: reading
  }).promise();
  
  return { statusCode: 201, body: JSON.stringify(reading) };
}

async function updateReading(dateCode, updates) {
  updates.updatedAt = new Date().toISOString();
  
  await dynamodb.update({
    TableName: 'BibleReadings',
    Key: { dateCode },
    UpdateExpression: 'SET #data = :data, updatedAt = :updatedAt',
    ExpressionAttributeNames: { '#data': 'data' },
    ExpressionAttributeValues: { ':data': updates, ':updatedAt': updates.updatedAt }
  }).promise();
  
  return { statusCode: 200, body: JSON.stringify({ dateCode, ...updates }) };
}

async function deleteReading(dateCode) {
  await dynamodb.delete({
    TableName: 'BibleReadings',
    Key: { dateCode }
  }).promise();
  
  return { statusCode: 204, body: '' };
}
```

## Step 3: Angular Admin Module

### Generate Admin Module
```bash
ng generate module admin --routing
ng generate component admin/dashboard
ng generate component admin/reading-form
ng generate component admin/reading-list
```

### Admin Service
```typescript
// src/app/admin/services/admin.service.ts
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Reading } from '../../models/reading.model';

@Injectable({
  providedIn: 'root'
})
export class AdminService {
  private apiUrl = 'https://your-api-gateway-url.amazonaws.com/prod';

  constructor(private http: HttpClient) {}

  getAllReadings(): Observable<Reading[]> {
    return this.http.get<Reading[]>(`${this.apiUrl}/readings`);
  }

  getReading(dateCode: string): Observable<Reading> {
    return this.http.get<Reading>(`${this.apiUrl}/readings/${dateCode}`);
  }

  createReading(reading: Reading): Observable<Reading> {
    return this.http.post<Reading>(`${this.apiUrl}/readings`, reading);
  }

  updateReading(dateCode: string, reading: Reading): Observable<Reading> {
    return this.http.put<Reading>(`${this.apiUrl}/readings/${dateCode}`, reading);
  }

  deleteReading(dateCode: string): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/readings/${dateCode}`);
  }

  uploadAudio(file: File): Observable<{url: string}> {
    const formData = new FormData();
    formData.append('file', file);
    return this.http.post<{url: string}>(`${this.apiUrl}/upload-audio`, formData);
  }
}
```

### Reading Form Component
```typescript
// src/app/admin/reading-form/reading-form.component.ts
import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, FormArray, Validators } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { AdminService } from '../services/admin.service';

@Component({
  selector: 'app-reading-form',
  templateUrl: './reading-form.component.html'
})
export class ReadingFormComponent implements OnInit {
  readingForm: FormGroup;
  isEdit = false;
  dateCode?: string;

  constructor(
    private fb: FormBuilder,
    private adminService: AdminService,
    private route: ActivatedRoute,
    private router: Router
  ) {
    this.readingForm = this.createForm();
  }

  ngOnInit(): void {
    this.dateCode = this.route.snapshot.params['dateCode'];
    if (this.dateCode) {
      this.isEdit = true;
      this.loadReading();
    }
  }

  createForm(): FormGroup {
    return this.fb.group({
      dateCode: ['', Validators.required],
      date: ['', Validators.required],
      dayOfWeek: ['', Validators.required],
      title: ['', Validators.required],
      audioUrl: [''],
      oldTestament: this.fb.array([]),
      newTestament: this.fb.array([])
    });
  }

  get oldTestamentArray(): FormArray {
    return this.readingForm.get('oldTestament') as FormArray;
  }

  get newTestamentArray(): FormArray {
    return this.readingForm.get('newTestament') as FormArray;
  }

  addScripture(testament: 'oldTestament' | 'newTestament'): void {
    const scriptureGroup = this.fb.group({
      book: ['', Validators.required],
      chapter: [''],
      verses: this.fb.array([])
    });
    
    if (testament === 'oldTestament') {
      this.oldTestamentArray.push(scriptureGroup);
    } else {
      this.newTestamentArray.push(scriptureGroup);
    }
  }

  addVerse(testamentIndex: number, testament: 'oldTestament' | 'newTestament'): void {
    const verseGroup = this.fb.group({
      number: ['', Validators.required],
      text: ['', Validators.required]
    });
    
    const scriptureArray = testament === 'oldTestament' ? this.oldTestamentArray : this.newTestamentArray;
    const versesArray = scriptureArray.at(testamentIndex).get('verses') as FormArray;
    versesArray.push(verseGroup);
  }

  onSubmit(): void {
    if (this.readingForm.valid) {
      const reading = this.readingForm.value;
      
      if (this.isEdit) {
        this.adminService.updateReading(this.dateCode!, reading).subscribe(() => {
          this.router.navigate(['/admin']);
        });
      } else {
        this.adminService.createReading(reading).subscribe(() => {
          this.router.navigate(['/admin']);
        });
      }
    }
  }

  onAudioUpload(event: any): void {
    const file = event.target.files[0];
    if (file) {
      this.adminService.uploadAudio(file).subscribe(response => {
        this.readingForm.patchValue({ audioUrl: response.url });
      });
    }
  }

  private loadReading(): void {
    this.adminService.getReading(this.dateCode!).subscribe(reading => {
      this.readingForm.patchValue(reading);
      // Populate form arrays for scriptures and verses
    });
  }
}
```

### Reading Form Template
```html
<!-- src/app/admin/reading-form/reading-form.component.html -->
<div class="container mt-4">
  <h2>{{ isEdit ? 'Edit' : 'Create' }} Reading</h2>
  
  <form [formGroup]="readingForm" (ngSubmit)="onSubmit()">
    <div class="row">
      <div class="col-md-6">
        <div class="mb-3">
          <label class="form-label">Date Code (MMDD)</label>
          <input type="text" class="form-control" formControlName="dateCode" 
                 placeholder="0922" [readonly]="isEdit">
        </div>
      </div>
      <div class="col-md-6">
        <div class="mb-3">
          <label class="form-label">Date</label>
          <input type="text" class="form-control" formControlName="date" 
                 placeholder="September 22">
        </div>
      </div>
    </div>

    <div class="row">
      <div class="col-md-6">
        <div class="mb-3">
          <label class="form-label">Day of Week</label>
          <select class="form-control" formControlName="dayOfWeek">
            <option value="Monday">Monday</option>
            <option value="Tuesday">Tuesday</option>
            <option value="Wednesday">Wednesday</option>
            <option value="Thursday">Thursday</option>
            <option value="Friday">Friday</option>
            <option value="Saturday">Saturday</option>
            <option value="Sunday">Sunday</option>
          </select>
        </div>
      </div>
      <div class="col-md-6">
        <div class="mb-3">
          <label class="form-label">Title</label>
          <input type="text" class="form-control" formControlName="title" 
                 placeholder="Song of Solomon 6:11 - Isaiah 1:31">
        </div>
      </div>
    </div>

    <div class="mb-3">
      <label class="form-label">Audio File</label>
      <input type="file" class="form-control" accept="audio/*" (change)="onAudioUpload($event)">
      <small class="form-text text-muted">Current: {{ readingForm.get('audioUrl')?.value }}</small>
    </div>

    <!-- Old Testament Section -->
    <div class="card mb-3">
      <div class="card-header d-flex justify-content-between">
        <h5>Old Testament</h5>
        <button type="button" class="btn btn-sm btn-primary" (click)="addScripture('oldTestament')">
          Add Scripture
        </button>
      </div>
      <div class="card-body">
        <div formArrayName="oldTestament">
          <div *ngFor="let scripture of oldTestamentArray.controls; let i = index" 
               [formGroupName]="i" class="border p-3 mb-3">
            <div class="row">
              <div class="col-md-6">
                <input type="text" class="form-control" formControlName="book" placeholder="Book Name">
              </div>
              <div class="col-md-6">
                <input type="text" class="form-control" formControlName="chapter" placeholder="Chapter:Verses">
              </div>
            </div>
            <div class="mt-2">
              <button type="button" class="btn btn-sm btn-secondary" (click)="addVerse(i, 'oldTestament')">
                Add Verse
              </button>
            </div>
            <!-- Verses would go here with similar FormArray structure -->
          </div>
        </div>
      </div>
    </div>

    <!-- New Testament Section (similar structure) -->

    <div class="d-flex gap-2">
      <button type="submit" class="btn btn-primary" [disabled]="!readingForm.valid">
        {{ isEdit ? 'Update' : 'Create' }} Reading
      </button>
      <button type="button" class="btn btn-secondary" (click)="router.navigate(['/admin'])">
        Cancel
      </button>
    </div>
  </form>
</div>
```

### Admin Dashboard
```typescript
// src/app/admin/dashboard/dashboard.component.ts
import { Component, OnInit } from '@angular/core';
import { AdminService } from '../services/admin.service';
import { Reading } from '../../models/reading.model';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html'
})
export class DashboardComponent implements OnInit {
  readings: Reading[] = [];
  loading = true;

  constructor(private adminService: AdminService) {}

  ngOnInit(): void {
    this.loadReadings();
  }

  loadReadings(): void {
    this.adminService.getAllReadings().subscribe(readings => {
      this.readings = readings.sort((a, b) => a.dateCode.localeCompare(b.dateCode));
      this.loading = false;
    });
  }

  deleteReading(dateCode: string): void {
    if (confirm('Are you sure you want to delete this reading?')) {
      this.adminService.deleteReading(dateCode).subscribe(() => {
        this.loadReadings();
      });
    }
  }
}
```

## Step 4: Authentication Guard

```typescript
// src/app/admin/guards/auth.guard.ts
import { Injectable } from '@angular/core';
import { CanActivate, Router } from '@angular/router';

@Injectable({
  providedIn: 'root'
})
export class AuthGuard implements CanActivate {
  constructor(private router: Router) {}

  canActivate(): boolean {
    // Simple password check - replace with proper auth
    const password = prompt('Enter admin password:');
    if (password === 'your-admin-password') {
      return true;
    }
    this.router.navigate(['/']);
    return false;
  }
}
```

## Step 5: Admin Routing

```typescript
// src/app/admin/admin-routing.module.ts
import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { DashboardComponent } from './dashboard/dashboard.component';
import { ReadingFormComponent } from './reading-form/reading-form.component';
import { AuthGuard } from './guards/auth.guard';

const routes: Routes = [
  { 
    path: '', 
    component: DashboardComponent, 
    canActivate: [AuthGuard] 
  },
  { 
    path: 'create', 
    component: ReadingFormComponent, 
    canActivate: [AuthGuard] 
  },
  { 
    path: 'edit/:dateCode', 
    component: ReadingFormComponent, 
    canActivate: [AuthGuard] 
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class AdminRoutingModule { }
```

## Step 6: Update Main App Routing

```typescript
// src/app/app-routing.module.ts
const routes: Routes = [
  { path: '', component: HomeComponent },
  { path: 'reading/:date', component: ReadingComponent },
  { path: 'coming-soon', component: ComingSoonComponent },
  { 
    path: 'admin', 
    loadChildren: () => import('./admin/admin.module').then(m => m.AdminModule) 
  },
  { path: '**', redirectTo: '' }
];
```

This creates a complete admin interface where you can:
- View all readings in a dashboard
- Create new readings with forms
- Edit existing readings
- Upload audio files
- Delete readings
- All data is stored in DynamoDB via Lambda functions

The admin section is protected and lazy-loaded for better performance.

---

Could you recreate the tutorial that includes the admin portion of the porject as well?

---


# Complete Angular One Year Bible with Admin - Step-by-Step Tutorial

## Prerequisites
- Node.js (v18+)
- Angular CLI
- AWS CLI configured
- AWS Account

## Part 1: Project Setup

### Step 1: Create Angular Project
```bash
npm install -g @angular/cli
ng new one-year-bible-admin --routing --style=scss
cd one-year-bible-admin
npm install bootstrap @angular/material
```

### Step 2: Configure Dependencies
**angular.json**
```json
"styles": [
  "node_modules/bootstrap/dist/css/bootstrap.min.css",
  "src/styles.scss"
],
"scripts": [
  "node_modules/bootstrap/dist/js/bootstrap.bundle.min.js"
]
```

**src/index.html**
```html
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600" rel="stylesheet">
```

## Part 2: Models and Interfaces

### Step 3: Create Models
**src/app/models/reading.model.ts**
```typescript
export interface Reading {
  dateCode: string;
  date: string;
  dayOfWeek: string;
  title: string;
  audioUrl?: string;
  oldTestament: Scripture[];
  newTestament: Scripture[];
  createdAt?: string;
  updatedAt?: string;
}

export interface Scripture {
  book: string;
  chapter?: string;
  verses: Verse[];
}

export interface Verse {
  number: number;
  text: string;
}

export interface ApiResponse<T> {
  data: T;
  message?: string;
  error?: string;
}
```

## Part 3: Core Services

### Step 4: Reading Service
**src/app/services/reading.service.ts**
```typescript
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, of } from 'rxjs';
import { Reading } from '../models/reading.model';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class ReadingService {
  private apiUrl = environment.apiUrl;

  constructor(private http: HttpClient) {}

  getAllReadings(): Observable<Reading[]> {
    return this.http.get<Reading[]>(`${this.apiUrl}/readings`);
  }

  getReading(dateCode: string): Observable<Reading | null> {
    return this.http.get<Reading>(`${this.apiUrl}/readings/${dateCode}`);
  }

  getAvailableReadings(): Observable<string[]> {
    return this.http.get<string[]>(`${this.apiUrl}/readings/available`);
  }
}
```

### Step 5: Admin Service
**src/app/services/admin.service.ts**
```typescript
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Reading } from '../models/reading.model';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class AdminService {
  private apiUrl = environment.apiUrl;

  constructor(private http: HttpClient) {}

  createReading(reading: Reading): Observable<Reading> {
    return this.http.post<Reading>(`${this.apiUrl}/admin/readings`, reading);
  }

  updateReading(dateCode: string, reading: Reading): Observable<Reading> {
    return this.http.put<Reading>(`${this.apiUrl}/admin/readings/${dateCode}`, reading);
  }

  deleteReading(dateCode: string): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/admin/readings/${dateCode}`);
  }

  uploadAudio(file: File): Observable<{url: string}> {
    const formData = new FormData();
    formData.append('file', file);
    return this.http.post<{url: string}>(`${this.apiUrl}/admin/upload-audio`, formData);
  }
}
```

### Step 6: Calendar Service
**src/app/services/calendar.service.ts**
```typescript
import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class CalendarService {
  private currentDate = new BehaviorSubject<Date>(new Date());
  currentDate$ = this.currentDate.asObservable();

  private months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];

  setCurrentDate(date: Date): void {
    this.currentDate.next(date);
  }

  getMonthName(monthIndex: number): string {
    return this.months[monthIndex];
  }

  generateCalendarDays(year: number, month: number): any[] {
    const firstDay = new Date(year, month, 1).getDay();
    const lastDate = new Date(year, month + 1, 0).getDate();
    const prevLastDate = new Date(year, month, 0).getDate();
    
    const days = [];
    
    for (let i = firstDay; i > 0; i--) {
      days.push({ day: prevLastDate - i + 1, inactive: true });
    }
    
    for (let i = 1; i <= lastDate; i++) {
      const isToday = this.isToday(year, month, i);
      days.push({ day: i, inactive: false, isToday });
    }
    
    return days;
  }

  private isToday(year: number, month: number, day: number): boolean {
    const today = new Date();
    return day === today.getDate() && 
           month === today.getMonth() && 
           year === today.getFullYear();
  }
}
```

## Part 4: Components

### Step 7: Calendar Widget Component
```bash
ng generate component components/calendar-widget
```

**src/app/components/calendar-widget/calendar-widget.component.ts**
```typescript
import { Component, Input, Output, EventEmitter, OnInit } from '@angular/core';
import { CalendarService } from '../../services/calendar.service';
import { ReadingService } from '../../services/reading.service';

@Component({
  selector: 'app-calendar-widget',
  templateUrl: './calendar-widget.component.html',
  styleUrls: ['./calendar-widget.component.scss']
})
export class CalendarWidgetComponent implements OnInit {
  @Input() currentPageDate?: string;
  @Output() dateSelected = new EventEmitter<string>();

  currentYear = new Date().getFullYear();
  currentMonth = new Date().getMonth();
  calendarDays: any[] = [];
  availableReadings: string[] = [];

  constructor(
    private calendarService: CalendarService,
    private readingService: ReadingService
  ) {}

  ngOnInit(): void {
    this.loadAvailableReadings();
    this.generateCalendar();
  }

  loadAvailableReadings(): void {
    this.readingService.getAvailableReadings().subscribe(readings => {
      this.availableReadings = readings;
    });
  }

  generateCalendar(): void {
    this.calendarDays = this.calendarService.generateCalendarDays(this.currentYear, this.currentMonth);
  }

  getMonthName(): string {
    return this.calendarService.getMonthName(this.currentMonth);
  }

  onDateClick(day: any): void {
    if (day.inactive) return;
    
    const monthStr = (this.currentMonth + 1).toString().padStart(2, '0');
    const dayStr = day.day.toString().padStart(2, '0');
    const dateCode = monthStr + dayStr;
    
    this.dateSelected.emit(dateCode);
  }

  previousMonth(): void {
    this.currentMonth--;
    if (this.currentMonth < 0) {
      this.currentMonth = 11;
      this.currentYear--;
    }
    this.generateCalendar();
  }

  nextMonth(): void {
    this.currentMonth++;
    if (this.currentMonth > 11) {
      this.currentMonth = 0;
      this.currentYear++;
    }
    this.generateCalendar();
  }

  isAvailable(day: any): boolean {
    if (day.inactive) return false;
    const monthStr = (this.currentMonth + 1).toString().padStart(2, '0');
    const dayStr = day.day.toString().padStart(2, '0');
    const dateCode = monthStr + dayStr;
    return this.availableReadings.includes(dateCode);
  }

  isCurrentPage(day: any): boolean {
    if (!this.currentPageDate || day.inactive) return false;
    const monthStr = (this.currentMonth + 1).toString().padStart(2, '0');
    const dayStr = day.day.toString().padStart(2, '0');
    const dateCode = monthStr + dayStr;
    return dateCode === this.currentPageDate;
  }
}
```

**src/app/components/calendar-widget/calendar-widget.component.html**
```html
<div class="calendar-widget-inline">
  <div class="widget-header">
    <span class="widget-current-date">{{ getMonthName() }} {{ currentYear }}</span>
    <div class="widget-navigation">
      <span class="material-symbols-rounded" (click)="previousMonth()">chevron_left</span>
      <span class="material-symbols-rounded" (click)="nextMonth()">chevron_right</span>
    </div>
  </div>
  <div class="widget-body">
    <ul class="widget-weekdays">
      <li>S</li><li>M</li><li>T</li><li>W</li><li>T</li><li>F</li><li>S</li>
    </ul>
    <ul class="widget-dates">
      <li *ngFor="let day of calendarDays" 
          [class.inactive]="day.inactive"
          [class.active]="day.isToday || isCurrentPage(day)"
          [class.available]="isAvailable(day)"
          (click)="onDateClick(day)">
        {{ day.day }}
      </li>
    </ul>
  </div>
</div>
```

### Step 8: Public Pages
```bash
ng generate component pages/home
ng generate component pages/reading
ng generate component pages/coming-soon
```

**src/app/pages/home/home.component.ts**
```typescript
import { Component } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent {
  constructor(private router: Router) {}

  onDateSelected(dateCode: string): void {
    this.router.navigate(['/reading', dateCode]);
  }

  goToToday(): void {
    const today = new Date();
    const monthStr = (today.getMonth() + 1).toString().padStart(2, '0');
    const dayStr = today.getDate().toString().padStart(2, '0');
    const dateCode = monthStr + dayStr;
    this.router.navigate(['/reading', dateCode]);
  }
}
```

**src/app/pages/home/home.component.html**
```html
<div class="container mt-5">
  <div class="text-center mb-5">
    <h1 class="display-4 mb-4">One Year Bible Reading Plan</h1>
    <p class="lead mb-4">
      Join us on a journey through the entire Bible in one year. Each day includes carefully selected readings 
      from the Old Testament, New Testament, Psalms, and Proverbs.
    </p>
    <p class="text-muted">
      This site follows the ONE-YEAR Bible guide found at 
      <a href="https://www.kcm.org/read/one-year-bible" target="_blank" rel="noopener noreferrer">
        Kenneth Copeland Ministries
      </a>
    </p>
  </div>

  <div class="row justify-content-center">
    <div class="col-lg-6 col-md-8">
      <app-calendar-widget (dateSelected)="onDateSelected($event)"></app-calendar-widget>
      <div class="text-center mt-3">
        <button class="btn btn-primary" (click)="goToToday()">Go to Today's Reading</button>
      </div>
    </div>
  </div>

  <div class="row mt-5">
    <div class="col-md-8 mx-auto">
      <div class="card">
        <div class="card-body">
          <h5 class="card-title">How to Use</h5>
          <ul class="list-unstyled">
            <li class="mb-2">📅 <strong>Click any date</strong> to go to that day's reading</li>
            <li class="mb-2">🎧 <strong>Audio available</strong> for most readings</li>
            <li class="mb-2">📖 <strong>Full scripture text</strong> included on each page</li>
            <li class="mb-2">⏭️ <strong>Navigate easily</strong> between days using the calendar</li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</div>
```

**src/app/pages/reading/reading.component.ts**
```typescript
import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { ReadingService } from '../../services/reading.service';
import { Reading } from '../../models/reading.model';

@Component({
  selector: 'app-reading',
  templateUrl: './reading.component.html',
  styleUrls: ['./reading.component.scss']
})
export class ReadingComponent implements OnInit {
  reading?: Reading;
  dateCode?: string;
  loading = true;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private readingService: ReadingService
  ) {}

  ngOnInit(): void {
    this.route.params.subscribe(params => {
      this.dateCode = params['date'];
      this.loadReading();
    });
  }

  loadReading(): void {
    if (!this.dateCode) return;
    
    this.readingService.getReading(this.dateCode).subscribe({
      next: (reading) => {
        if (reading) {
          this.reading = reading;
        } else {
          this.router.navigate(['/coming-soon'], { queryParams: { date: this.dateCode } });
        }
        this.loading = false;
      },
      error: () => {
        this.router.navigate(['/coming-soon'], { queryParams: { date: this.dateCode } });
        this.loading = false;
      }
    });
  }

  onDateSelected(dateCode: string): void {
    this.router.navigate(['/reading', dateCode]);
  }
}
```

## Part 5: Admin Module

### Step 9: Create Admin Module
```bash
ng generate module admin --routing
ng generate component admin/dashboard
ng generate component admin/reading-form
ng generate component admin/reading-list
ng generate guard admin/guards/auth
```

### Step 10: Auth Guard
**src/app/admin/guards/auth.guard.ts**
```typescript
import { Injectable } from '@angular/core';
import { CanActivate, Router } from '@angular/router';

@Injectable({
  providedIn: 'root'
})
export class AuthGuard implements CanActivate {
  constructor(private router: Router) {}

  canActivate(): boolean {
    const isAuthenticated = localStorage.getItem('admin-auth') === 'true';
    
    if (!isAuthenticated) {
      const password = prompt('Enter admin password:');
      if (password === 'admin123') { // Replace with secure auth
        localStorage.setItem('admin-auth', 'true');
        return true;
      }
      this.router.navigate(['/']);
      return false;
    }
    
    return true;
  }
}
```

### Step 11: Admin Dashboard
**src/app/admin/dashboard/dashboard.component.ts**
```typescript
import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { AdminService } from '../../services/admin.service';
import { ReadingService } from '../../services/reading.service';
import { Reading } from '../../models/reading.model';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss']
})
export class DashboardComponent implements OnInit {
  readings: Reading[] = [];
  loading = true;

  constructor(
    private adminService: AdminService,
    private readingService: ReadingService,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.loadReadings();
  }

  loadReadings(): void {
    this.readingService.getAllReadings().subscribe({
      next: (readings) => {
        this.readings = readings.sort((a, b) => a.dateCode.localeCompare(b.dateCode));
        this.loading = false;
      },
      error: () => {
        this.loading = false;
      }
    });
  }

  editReading(dateCode: string): void {
    this.router.navigate(['/admin/edit', dateCode]);
  }

  deleteReading(dateCode: string): void {
    if (confirm('Are you sure you want to delete this reading?')) {
      this.adminService.deleteReading(dateCode).subscribe(() => {
        this.loadReadings();
      });
    }
  }

  logout(): void {
    localStorage.removeItem('admin-auth');
    this.router.navigate(['/']);
  }
}
```

**src/app/admin/dashboard/dashboard.component.html**
```html
<div class="container mt-4">
  <div class="d-flex justify-content-between align-items-center mb-4">
    <h2>Admin Dashboard</h2>
    <div>
      <button class="btn btn-primary me-2" routerLink="/admin/create">Create Reading</button>
      <button class="btn btn-outline-secondary" (click)="logout()">Logout</button>
    </div>
  </div>

  <div *ngIf="loading" class="text-center">
    <div class="spinner-border" role="status"></div>
  </div>

  <div *ngIf="!loading" class="row">
    <div class="col-12">
      <div class="card">
        <div class="card-header">
          <h5>Bible Readings ({{ readings.length }})</h5>
        </div>
        <div class="card-body">
          <div class="table-responsive">
            <table class="table table-striped">
              <thead>
                <tr>
                  <th>Date Code</th>
                  <th>Date</th>
                  <th>Title</th>
                  <th>Audio</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr *ngFor="let reading of readings">
                  <td>{{ reading.dateCode }}</td>
                  <td>{{ reading.date }}</td>
                  <td>{{ reading.title }}</td>
                  <td>
                    <span class="badge" [class]="reading.audioUrl ? 'bg-success' : 'bg-secondary'">
                      {{ reading.audioUrl ? 'Yes' : 'No' }}
                    </span>
                  </td>
                  <td>
                    <button class="btn btn-sm btn-outline-primary me-1" (click)="editReading(reading.dateCode)">
                      Edit
                    </button>
                    <button class="btn btn-sm btn-outline-danger" (click)="deleteReading(reading.dateCode)">
                      Delete
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>
```

### Step 12: Reading Form Component
**src/app/admin/reading-form/reading-form.component.ts**
```typescript
import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, FormArray, Validators } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { AdminService } from '../../services/admin.service';
import { ReadingService } from '../../services/reading.service';

@Component({
  selector: 'app-reading-form',
  templateUrl: './reading-form.component.html',
  styleUrls: ['./reading-form.component.scss']
})
export class ReadingFormComponent implements OnInit {
  readingForm: FormGroup;
  isEdit = false;
  dateCode?: string;
  loading = false;

  constructor(
    private fb: FormBuilder,
    private adminService: AdminService,
    private readingService: ReadingService,
    private route: ActivatedRoute,
    private router: Router
  ) {
    this.readingForm = this.createForm();
  }

  ngOnInit(): void {
    this.dateCode = this.route.snapshot.params['dateCode'];
    if (this.dateCode) {
      this.isEdit = true;
      this.loadReading();
    }
  }

  createForm(): FormGroup {
    return this.fb.group({
      dateCode: ['', [Validators.required, Validators.pattern(/^\d{4}$/)]],
      date: ['', Validators.required],
      dayOfWeek: ['', Validators.required],
      title: ['', Validators.required],
      audioUrl: [''],
      oldTestament: this.fb.array([]),
      newTestament: this.fb.array([])
    });
  }

  get oldTestamentArray(): FormArray {
    return this.readingForm.get('oldTestament') as FormArray;
  }

  get newTestamentArray(): FormArray {
    return this.readingForm.get('newTestament') as FormArray;
  }

  addScripture(testament: 'oldTestament' | 'newTestament'): void {
    const scriptureGroup = this.fb.group({
      book: ['', Validators.required],
      chapter: [''],
      verses: this.fb.array([this.createVerseGroup()])
    });
    
    if (testament === 'oldTestament') {
      this.oldTestamentArray.push(scriptureGroup);
    } else {
      this.newTestamentArray.push(scriptureGroup);
    }
  }

  createVerseGroup(): FormGroup {
    return this.fb.group({
      number: ['', Validators.required],
      text: ['', Validators.required]
    });
  }

  addVerse(testamentIndex: number, testament: 'oldTestament' | 'newTestament'): void {
    const scriptureArray = testament === 'oldTestament' ? this.oldTestamentArray : this.newTestamentArray;
    const versesArray = scriptureArray.at(testamentIndex).get('verses') as FormArray;
    versesArray.push(this.createVerseGroup());
  }

  removeVerse(testamentIndex: number, verseIndex: number, testament: 'oldTestament' | 'newTestament'): void {
    const scriptureArray = testament === 'oldTestament' ? this.oldTestamentArray : this.newTestamentArray;
    const versesArray = scriptureArray.at(testamentIndex).get('verses') as FormArray;
    versesArray.removeAt(verseIndex);
  }

  removeScripture(index: number, testament: 'oldTestament' | 'newTestament'): void {
    if (testament === 'oldTestament') {
      this.oldTestamentArray.removeAt(index);
    } else {
      this.newTestamentArray.removeAt(index);
    }
  }

  onSubmit(): void {
    if (this.readingForm.valid) {
      this.loading = true;
      const reading = this.readingForm.value;
      
      const operation = this.isEdit 
        ? this.adminService.updateReading(this.dateCode!, reading)
        : this.adminService.createReading(reading);
      
      operation.subscribe({
        next: () => {
          this.router.navigate(['/admin']);
        },
        error: (error) => {
          console.error('Error saving reading:', error);
          this.loading = false;
        }
      });
    }
  }

  onAudioUpload(event: any): void {
    const file = event.target.files[0];
    if (file) {
      this.adminService.uploadAudio(file).subscribe({
        next: (response) => {
          this.readingForm.patchValue({ audioUrl: response.url });
        },
        error: (error) => {
          console.error('Error uploading audio:', error);
        }
      });
    }
  }

  private loadReading(): void {
    this.readingService.getReading(this.dateCode!).subscribe({
      next: (reading) => {
        if (reading) {
          this.populateForm(reading);
        }
      },
      error: (error) => {
        console.error('Error loading reading:', error);
      }
    });
  }

  private populateForm(reading: any): void {
    this.readingForm.patchValue({
      dateCode: reading.dateCode,
      date: reading.date,
      dayOfWeek: reading.dayOfWeek,
      title: reading.title,
      audioUrl: reading.audioUrl
    });

    // Populate Old Testament
    reading.oldTestament?.forEach((scripture: any) => {
      const scriptureGroup = this.fb.group({
        book: [scripture.book],
        chapter: [scripture.chapter],
        verses: this.fb.array([])
      });
      
      const versesArray = scriptureGroup.get('verses') as FormArray;
      scripture.verses?.forEach((verse: any) => {
        versesArray.push(this.fb.group({
          number: [verse.number],
          text: [verse.text]
        }));
      });
      
      this.oldTestamentArray.push(scriptureGroup);
    });

    // Populate New Testament (similar logic)
    reading.newTestament?.forEach((scripture: any) => {
      const scriptureGroup = this.fb.group({
        book: [scripture.book],
        chapter: [scripture.chapter],
        verses: this.fb.array([])
      });
      
      const versesArray = scriptureGroup.get('verses') as FormArray;
      scripture.verses?.forEach((verse: any) => {
        versesArray.push(this.fb.group({
          number: [verse.number],
          text: [verse.text]
        }));
      });
      
      this.newTestamentArray.push(scriptureGroup);
    });
  }

  getVersesArray(testamentIndex: number, testament: 'oldTestament' | 'newTestament'): FormArray {
    const scriptureArray = testament === 'oldTestament' ? this.oldTestamentArray : this.newTestamentArray;
    return scriptureArray.at(testamentIndex).get('verses') as FormArray;
  }
}
```

**src/app/admin/reading-form/reading-form.component.html**
```html
<div class="container mt-4">
  <div class="d-flex justify-content-between align-items-center mb-4">
    <h2>{{ isEdit ? 'Edit' : 'Create' }} Reading</h2>
    <button class="btn btn-outline-secondary" routerLink="/admin">Back to Dashboard</button>
  </div>

  <form [formGroup]="readingForm" (ngSubmit)="onSubmit()">
    <!-- Basic Information -->
    <div class="card mb-4">
      <div class="card-header">
        <h5>Basic Information</h5>
      </div>
      <div class="card-body">
        <div class="row">
          <div class="col-md-3">
            <div class="mb-3">
              <label class="form-label">Date Code (MMDD)</label>
              <input type="text" class="form-control" formControlName="dateCode" 
                     placeholder="0922" [readonly]="isEdit">
              <div class="form-text">Format: MMDD (e.g., 0922 for September 22)</div>
            </div>
          </div>
          <div class="col-md-3">
            <div class="mb-3">
              <label class="form-label">Date</label>
              <input type="text" class="form-control" formControlName="date" 
                     placeholder="September 22">
            </div>
          </div>
          <div class="col-md-3">
            <div class="mb-3">
              <label class="form-label">Day of Week</label>
              <select class="form-control" formControlName="dayOfWeek">
                <option value="">Select Day</option>
                <option value="Monday">Monday</option>
                <option value="Tuesday">Tuesday</option>
                <option value="Wednesday">Wednesday</option>
                <option value="Thursday">Thursday</option>
                <option value="Friday">Friday</option>
                <option value="Saturday">Saturday</option>
                <option value="Sunday">Sunday</option>
              </select>
            </div>
          </div>
          <div class="col-md-3">
            <div class="mb-3">
              <label class="form-label">Title</label>
              <input type="text" class="form-control" formControlName="title" 
                     placeholder="Song of Solomon 6:11 - Isaiah 1:31">
            </div>
          </div>
        </div>

        <div class="mb-3">
          <label class="form-label">Audio File</label>
          <input type="file" class="form-control" accept="audio/*" (change)="onAudioUpload($event)">
          <div class="form-text" *ngIf="readingForm.get('audioUrl')?.value">
            Current: {{ readingForm.get('audioUrl')?.value }}
          </div>
        </div>
      </div>
    </div>

    <!-- Old Testament -->
    <div class="card mb-4">
      <div class="card-header d-flex justify-content-between align-items-center">
        <h5>Old Testament</h5>
        <button type="button" class="btn btn-sm btn-primary" (click)="addScripture('oldTestament')">
          Add Scripture
        </button>
      </div>
      <div class="card-body">
        <div formArrayName="oldTestament">
          <div *ngFor="let scripture of oldTestamentArray.controls; let i = index" 
               [formGroupName]="i" class="border p-3 mb-3">
            <div class="d-flex justify-content-between align-items-center mb-2">
              <h6>Scripture {{ i + 1 }}</h6>
              <button type="button" class="btn btn-sm btn-outline-danger" 
                      (click)="removeScripture(i, 'oldTestament')">
                Remove
              </button>
            </div>
            
            <div class="row mb-2">
              <div class="col-md-6">
                <input type="text" class="form-control" formControlName="book" 
                       placeholder="Book Name (e.g., Song of Solomon)">
              </div>
              <div class="col-md-6">
                <input type="text" class="form-control" formControlName="chapter" 
                       placeholder="Chapter:Verses (e.g., 6:11-13)">
              </div>
            </div>

            <!-- Verses -->
            <div formArrayName="verses">
              <div class="d-flex justify-content-between align-items-center mb-2">
                <strong>Verses</strong>
                <button type="button" class="btn btn-sm btn-secondary" 
                        (click)="addVerse(i, 'oldTestament')">
                  Add Verse
                </button>
              </div>
              
              <div *ngFor="let verse of getVersesArray(i, 'oldTestament').controls; let j = index" 
                   [formGroupName]="j" class="row mb-2">
                <div class="col-md-2">
                  <input type="number" class="form-control" formControlName="number" 
                         placeholder="Verse #">
                </div>
                <div class="col-md-9">
                  <textarea class="form-control" formControlName="text" rows="2" 
                            placeholder="Verse text"></textarea>
                </div>
                <div class="col-md-1">
                  <button type="button" class="btn btn-sm btn-outline-danger" 
                          (click)="removeVerse(i, j, 'oldTestament')">
                    ×
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- New Testament (similar structure) -->
    <div class="card mb-4">
      <div class="card-header d-flex justify-content-between align-items-center">
        <h5>New Testament</h5>
        <button type="button" class="btn btn-sm btn-primary" (click)="addScripture('newTestament')">
          Add Scripture
        </button>
      </div>
      <div class="card-body">
        <div formArrayName="newTestament">
          <div *ngFor="let scripture of newTestamentArray.controls; let i = index" 
               [formGroupName]="i" class="border p-3 mb-3">
            <div class="d-flex justify-content-between align-items-center mb-2">
              <h6>Scripture {{ i + 1 }}</h6>
              <button type="button" class="btn btn-sm btn-outline-danger" 
                      (click)="removeScripture(i, 'newTestament')">
                Remove
              </button>
            </div>
            
            <div class="row mb-2">
              <div class="col-md-6">
                <input type="text" class="form-control" formControlName="book" 
                       placeholder="Book Name">
              </div>
              <div class="col-md-6">
                <input type="text" class="form-control" formControlName="chapter" 
                       placeholder="Chapter:Verses">
              </div>
            </div>

            <div formArrayName="verses">
              <div class="d-flex justify-content-between align-items-center mb-2">
                <strong>Verses</strong>
                <button type="button" class="btn btn-sm btn-secondary" 
                        (click)="addVerse(i, 'newTestament')">
                  Add Verse
                </button>
              </div>
              
              <div *ngFor="let verse of getVersesArray(i, 'newTestament').controls; let j = index" 
                   [formGroupName]="j" class="row mb-2">
                <div class="col-md-2">
                  <input type="number" class="form-control" formControlName="number" 
                         placeholder="Verse #">
                </div>
                <div class="col-md-9">
                  <textarea class="form-control" formControlName="text" rows="2" 
                            placeholder="Verse text"></textarea>
                </div>
                <div class="col-md-1">
                  <button type="button" class="btn btn-sm btn-outline-danger" 
                          (click)="removeVerse(i, j, 'newTestament')">
                    ×
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Submit Buttons -->
    <div class="d-flex gap-2 mb-4">
      <button type="submit" class="btn btn-primary" [disabled]="!readingForm.valid || loading">
        <span *ngIf="loading" class="spinner-border spinner-border-sm me-2"></span>
        {{ isEdit ? 'Update' : 'Create' }} Reading
      </button>
      <button type="button" class="btn btn-secondary" routerLink="/admin">
        Cancel
      </button>
    </div>
  </form>
</div>
```

### Step 13: Admin Routing
**src/app/admin/admin-routing.module.ts**
```typescript
import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { DashboardComponent } from './dashboard/dashboard.component';
import { ReadingFormComponent } from './reading-form/reading-form.component';
import { AuthGuard } from './guards/auth.guard';

const routes: Routes = [
  { 
    path: '', 
    component: DashboardComponent, 
    canActivate: [AuthGuard] 
  },
  { 
    path: 'create', 
    component: ReadingFormComponent, 
    canActivate: [AuthGuard] 
  },
  { 
    path: 'edit/:dateCode', 
    component: ReadingFormComponent, 
    canActivate: [AuthGuard] 
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class AdminRoutingModule { }
```

**src/app/admin/admin.module.ts**
```typescript
import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule } from '@angular/forms';

import { AdminRoutingModule } from './admin-routing.module';
import { DashboardComponent } from './dashboard/dashboard.component';
import { ReadingFormComponent } from './reading-form/reading-form.component';
import { ReadingListComponent } from './reading-list/reading-list.component';

@NgModule({
  declarations: [
    DashboardComponent,
    ReadingFormComponent,
    ReadingListComponent
  ],
  imports: [
    CommonModule,
    ReactiveFormsModule,
    AdminRoutingModule
  ]
})
export class AdminModule { }
```

## Part 6: Main App Configuration

### Step 14: App Routing
**src/app/app-routing.module.ts**
```typescript
import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { HomeComponent } from './pages/home/home.component';
import { ReadingComponent } from './pages/reading/reading.component';
import { ComingSoonComponent } from './pages/coming-soon/coming-soon.component';

const routes: Routes = [
  { path: '', component: HomeComponent },
  { path: 'reading/:date', component: ReadingComponent },
  { path: 'coming-soon', component: ComingSoonComponent },
  { 
    path: 'admin', 
    loadChildren: () => import('./admin/admin.module').then(m => m.AdminModule) 
  },
  { path: '**', redirectTo: '' }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
```

### Step 15: App Module
**src/app/app.module.ts**
```typescript
import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http';
import { ReactiveFormsModule } from '@angular/forms';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { HomeComponent } from './pages/home/home.component';
import { ReadingComponent } from './pages/reading/reading.component';
import { ComingSoonComponent } from './pages/coming-soon/coming-soon.component';
import { CalendarWidgetComponent } from './components/calendar-widget/calendar-widget.component';

@NgModule({
  declarations: [
    AppComponent,
    HomeComponent,
    ReadingComponent,
    ComingSoonComponent,
    CalendarWidgetComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    ReactiveFormsModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
```

### Step 16: Environment Configuration
**src/environments/environment.ts**
```typescript
export const environment = {
  production: false,
  apiUrl: 'http://localhost:3000/api' // Local development
};
```

**src/environments/environment.prod.ts**
```typescript
export const environment = {
  production: true,
  apiUrl: 'https://your-api-gateway-url.amazonaws.com/prod'
};
```

### Step 17: Copy Styles
Copy your existing CSS files to `src/assets/styles/` and update `src/styles.scss`:

```scss
@import 'assets/styles/widget-style.css';
@import 'assets/styles/scripture-style.css';

// Additional admin styles
.admin-nav {
  background-color: #343a40;
}

.calendar-widget-inline {
  max-width: 300px;
  margin: 0 auto;
}
```

## Part 7: Build and Deploy

### Step 18: Build Application
```bash
# Development
ng serve

# Production build
ng build --prod

# Test admin functionality
# Navigate to http://localhost:4200/admin
```

This complete tutorial creates a full-featured Angular application with:

- **Public Interface**: Home page, reading pages, calendar navigation
- **Admin Interface**: Dashboard, CRUD operations, file uploads
- **Authentication**: Simple password protection for admin
- **Responsive Design**: Bootstrap-based UI
- **Modular Architecture**: Lazy-loaded admin module
- **API Ready**: Structured for AWS Lambda backend integration

The admin interface allows you to:
- Create new Bible readings with scripture text
- Edit existing readings
- Upload audio files
- Delete readings
- View all readings in a dashboard

Next steps would be implementing the AWS Lambda backend and DynamoDB integration.

---

Could you add the lambda backend and the dynmaodb integration to the tutorial?

---


# Complete Angular One Year Bible with AWS Lambda Backend - Full Tutorial

## Part 8: AWS Lambda Backend Setup

### Step 19: Create AWS Infrastructure

#### Create DynamoDB Table
```bash
aws dynamodb create-table \
  --table-name BibleReadings \
  --attribute-definitions \
    AttributeName=dateCode,AttributeType=S \
  --key-schema \
    AttributeName=dateCode,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST \
  --region us-east-1
```

#### Create S3 Bucket for Audio Files
```bash
aws s3 mb s3://one-year-bible-audio-files
aws s3api put-bucket-cors --bucket one-year-bible-audio-files --cors-configuration file://cors.json
```

**cors.json**
```json
{
  "CORSRules": [
    {
      "AllowedOrigins": ["*"],
      "AllowedHeaders": ["*"],
      "AllowedMethods": ["GET", "PUT", "POST", "DELETE"],
      "MaxAgeSeconds": 3000
    }
  ]
}
```

### Step 20: Lambda Functions

#### Main CRUD Lambda Function
**lambda/readings-crud/index.js**
```javascript
const AWS = require('aws-sdk');
const dynamodb = new AWS.DynamoDB.DocumentClient();

const CORS_HEADERS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
  'Access-Control-Allow-Methods': 'GET,POST,PUT,DELETE,OPTIONS'
};

exports.handler = async (event) => {
  console.log('Event:', JSON.stringify(event, null, 2));
  
  // Handle CORS preflight
  if (event.httpMethod === 'OPTIONS') {
    return {
      statusCode: 200,
      headers: CORS_HEADERS,
      body: ''
    };
  }

  const { httpMethod, pathParameters, body, path } = event;
  const dateCode = pathParameters?.dateCode;
  
  try {
    let result;
    
    switch (httpMethod) {
      case 'GET':
        if (path.includes('/available')) {
          result = await getAvailableReadings();
        } else {
          result = await getReading(dateCode);
        }
        break;
      case 'POST':
        result = await createReading(JSON.parse(body));
        break;
      case 'PUT':
        result = await updateReading(dateCode, JSON.parse(body));
        break;
      case 'DELETE':
        result = await deleteReading(dateCode);
        break;
      default:
        result = { statusCode: 405, body: JSON.stringify({ error: 'Method Not Allowed' }) };
    }
    
    return {
      ...result,
      headers: CORS_HEADERS
    };
    
  } catch (error) {
    console.error('Error:', error);
    return {
      statusCode: 500,
      headers: CORS_HEADERS,
      body: JSON.stringify({ error: error.message })
    };
  }
};

async function getReading(dateCode) {
  if (dateCode) {
    const result = await dynamodb.get({
      TableName: 'BibleReadings',
      Key: { dateCode }
    }).promise();
    
    return {
      statusCode: result.Item ? 200 : 404,
      body: JSON.stringify(result.Item || { error: 'Reading not found' })
    };
  } else {
    const result = await dynamodb.scan({
      TableName: 'BibleReadings'
    }).promise();
    
    return {
      statusCode: 200,
      body: JSON.stringify(result.Items || [])
    };
  }
}

async function getAvailableReadings() {
  const result = await dynamodb.scan({
    TableName: 'BibleReadings',
    ProjectionExpression: 'dateCode'
  }).promise();
  
  const dateCodes = result.Items.map(item => item.dateCode).sort();
  
  return {
    statusCode: 200,
    body: JSON.stringify(dateCodes)
  };
}

async function createReading(reading) {
  // Validate required fields
  if (!reading.dateCode || !reading.date || !reading.title) {
    return {
      statusCode: 400,
      body: JSON.stringify({ error: 'Missing required fields: dateCode, date, title' })
    };
  }
  
  reading.createdAt = new Date().toISOString();
  reading.updatedAt = new Date().toISOString();
  
  await dynamodb.put({
    TableName: 'BibleReadings',
    Item: reading,
    ConditionExpression: 'attribute_not_exists(dateCode)' // Prevent overwrite
  }).promise();
  
  return {
    statusCode: 201,
    body: JSON.stringify(reading)
  };
}

async function updateReading(dateCode, updates) {
  if (!dateCode) {
    return {
      statusCode: 400,
      body: JSON.stringify({ error: 'dateCode is required' })
    };
  }
  
  updates.updatedAt = new Date().toISOString();
  
  // Build update expression dynamically
  const updateExpressions = [];
  const expressionAttributeNames = {};
  const expressionAttributeValues = {};
  
  Object.keys(updates).forEach(key => {
    if (key !== 'dateCode') { // Don't update the key
      updateExpressions.push(`#${key} = :${key}`);
      expressionAttributeNames[`#${key}`] = key;
      expressionAttributeValues[`:${key}`] = updates[key];
    }
  });
  
  const result = await dynamodb.update({
    TableName: 'BibleReadings',
    Key: { dateCode },
    UpdateExpression: `SET ${updateExpressions.join(', ')}`,
    ExpressionAttributeNames: expressionAttributeNames,
    ExpressionAttributeValues: expressionAttributeValues,
    ReturnValues: 'ALL_NEW'
  }).promise();
  
  return {
    statusCode: 200,
    body: JSON.stringify(result.Attributes)
  };
}

async function deleteReading(dateCode) {
  if (!dateCode) {
    return {
      statusCode: 400,
      body: JSON.stringify({ error: 'dateCode is required' })
    };
  }
  
  await dynamodb.delete({
    TableName: 'BibleReadings',
    Key: { dateCode }
  }).promise();
  
  return {
    statusCode: 204,
    body: ''
  };
}
```

#### Audio Upload Lambda Function
**lambda/audio-upload/index.js**
```javascript
const AWS = require('aws-sdk');
const s3 = new AWS.S3();
const { v4: uuidv4 } = require('uuid');

const CORS_HEADERS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
  'Access-Control-Allow-Methods': 'POST,OPTIONS'
};

exports.handler = async (event) => {
  if (event.httpMethod === 'OPTIONS') {
    return {
      statusCode: 200,
      headers: CORS_HEADERS,
      body: ''
    };
  }

  try {
    const { filename, contentType } = JSON.parse(event.body);
    
    if (!filename || !contentType) {
      return {
        statusCode: 400,
        headers: CORS_HEADERS,
        body: JSON.stringify({ error: 'filename and contentType are required' })
      };
    }

    const key = `audio/${uuidv4()}-${filename}`;
    const bucketName = 'one-year-bible-audio-files';
    
    // Generate presigned URL for upload
    const uploadUrl = s3.getSignedUrl('putObject', {
      Bucket: bucketName,
      Key: key,
      ContentType: contentType,
      Expires: 300 // 5 minutes
    });
    
    // Generate the final URL for the uploaded file
    const fileUrl = `https://${bucketName}.s3.amazonaws.com/${key}`;
    
    return {
      statusCode: 200,
      headers: CORS_HEADERS,
      body: JSON.stringify({
        uploadUrl,
        fileUrl,
        key
      })
    };
    
  } catch (error) {
    console.error('Error:', error);
    return {
      statusCode: 500,
      headers: CORS_HEADERS,
      body: JSON.stringify({ error: error.message })
    };
  }
};
```

### Step 21: Deploy Lambda Functions

#### Package and Deploy CRUD Lambda
```bash
# Create deployment package
mkdir lambda-deploy
cd lambda-deploy

# Copy function code
cp ../lambda/readings-crud/index.js .

# Create package.json
cat > package.json << EOF
{
  "name": "readings-crud",
  "version": "1.0.0",
  "dependencies": {
    "aws-sdk": "^2.1000.0"
  }
}
EOF

# Install dependencies and create zip
npm install
zip -r readings-crud.zip .

# Deploy to AWS
aws lambda create-function \
  --function-name readings-crud \
  --runtime nodejs18.x \
  --role arn:aws:iam::YOUR_ACCOUNT_ID:role/lambda-execution-role \
  --handler index.handler \
  --zip-file fileb://readings-crud.zip \
  --timeout 30 \
  --memory-size 256

# Deploy audio upload function similarly
cd ../
mkdir audio-upload-deploy
cd audio-upload-deploy
cp ../lambda/audio-upload/index.js .

cat > package.json << EOF
{
  "name": "audio-upload",
  "version": "1.0.0",
  "dependencies": {
    "aws-sdk": "^2.1000.0",
    "uuid": "^9.0.0"
  }
}
EOF

npm install
zip -r audio-upload.zip .

aws lambda create-function \
  --function-name audio-upload \
  --runtime nodejs18.x \
  --role arn:aws:iam::YOUR_ACCOUNT_ID:role/lambda-execution-role \
  --handler index.handler \
  --zip-file fileb://audio-upload.zip
```

### Step 22: Create IAM Role for Lambda

**lambda-execution-role-policy.json**
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": "arn:aws:logs:*:*:*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "dynamodb:GetItem",
        "dynamodb:PutItem",
        "dynamodb:UpdateItem",
        "dynamodb:DeleteItem",
        "dynamodb:Scan",
        "dynamodb:Query"
      ],
      "Resource": "arn:aws:dynamodb:*:*:table/BibleReadings"
    },
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:PutObject",
        "s3:DeleteObject"
      ],
      "Resource": "arn:aws:s3:::one-year-bible-audio-files/*"
    }
  ]
}
```

```bash
# Create IAM role
aws iam create-role \
  --role-name lambda-execution-role \
  --assume-role-policy-document '{
    "Version": "2012-10-17",
    "Statement": [
      {
        "Effect": "Allow",
        "Principal": {
          "Service": "lambda.amazonaws.com"
        },
        "Action": "sts:AssumeRole"
      }
    ]
  }'

# Attach policy
aws iam put-role-policy \
  --role-name lambda-execution-role \
  --policy-name lambda-execution-policy \
  --policy-document file://lambda-execution-role-policy.json
```

### Step 23: Create API Gateway

```bash
# Create REST API
aws apigateway create-rest-api \
  --name one-year-bible-api \
  --description "One Year Bible Reading API"

# Get API ID (replace with actual ID from above command)
API_ID="your-api-id"

# Get root resource ID
ROOT_ID=$(aws apigateway get-resources --rest-api-id $API_ID --query 'items[0].id' --output text)

# Create /readings resource
aws apigateway create-resource \
  --rest-api-id $API_ID \
  --parent-id $ROOT_ID \
  --path-part readings

# Get readings resource ID
READINGS_ID=$(aws apigateway get-resources --rest-api-id $API_ID --query 'items[?pathPart==`readings`].id' --output text)

# Create /readings/{dateCode} resource
aws apigateway create-resource \
  --rest-api-id $API_ID \
  --parent-id $READINGS_ID \
  --path-part "{dateCode}"

# Get dateCode resource ID
DATECODE_ID=$(aws apigateway get-resources --rest-api-id $API_ID --query 'items[?pathPart==`{dateCode}`].id' --output text)

# Create /readings/available resource
aws apigateway create-resource \
  --rest-api-id $API_ID \
  --parent-id $READINGS_ID \
  --path-part available

# Add methods and integrations (example for GET /readings)
aws apigateway put-method \
  --rest-api-id $API_ID \
  --resource-id $READINGS_ID \
  --http-method GET \
  --authorization-type NONE

aws apigateway put-integration \
  --rest-api-id $API_ID \
  --resource-id $READINGS_ID \
  --http-method GET \
  --type AWS_PROXY \
  --integration-http-method POST \
  --uri arn:aws:apigateway:us-east-1:lambda:path/2015-03-31/functions/arn:aws:lambda:us-east-1:YOUR_ACCOUNT_ID:function:readings-crud/invocations

# Deploy API
aws apigateway create-deployment \
  --rest-api-id $API_ID \
  --stage-name prod
```

### Step 24: Update Angular Services for AWS Integration

**src/app/services/reading.service.ts**
```typescript
import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError, map } from 'rxjs/operators';
import { Reading } from '../models/reading.model';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class ReadingService {
  private apiUrl = environment.apiUrl;

  constructor(private http: HttpClient) {}

  getAllReadings(): Observable<Reading[]> {
    return this.http.get<Reading[]>(`${this.apiUrl}/readings`)
      .pipe(
        catchError(this.handleError)
      );
  }

  getReading(dateCode: string): Observable<Reading | null> {
    return this.http.get<Reading>(`${this.apiUrl}/readings/${dateCode}`)
      .pipe(
        map(response => response || null),
        catchError((error: HttpErrorResponse) => {
          if (error.status === 404) {
            return [null]; // Return null for not found
          }
          return throwError(error);
        })
      );
  }

  getAvailableReadings(): Observable<string[]> {
    return this.http.get<string[]>(`${this.apiUrl}/readings/available`)
      .pipe(
        catchError(this.handleError)
      );
  }

  private handleError(error: HttpErrorResponse) {
    console.error('API Error:', error);
    return throwError(error);
  }
}
```

**src/app/services/admin.service.ts**
```typescript
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Reading } from '../models/reading.model';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class AdminService {
  private apiUrl = environment.apiUrl;

  constructor(private http: HttpClient) {}

  createReading(reading: Reading): Observable<Reading> {
    return this.http.post<Reading>(`${this.apiUrl}/readings`, reading);
  }

  updateReading(dateCode: string, reading: Reading): Observable<Reading> {
    return this.http.put<Reading>(`${this.apiUrl}/readings/${dateCode}`, reading);
  }

  deleteReading(dateCode: string): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/readings/${dateCode}`);
  }

  uploadAudio(file: File): Observable<{url: string}> {
    // First, get presigned URL
    const uploadRequest = {
      filename: file.name,
      contentType: file.type
    };

    return new Observable(observer => {
      this.http.post<any>(`${this.apiUrl}/upload-audio`, uploadRequest)
        .subscribe({
          next: (response) => {
            // Upload file to S3 using presigned URL
            const formData = new FormData();
            formData.append('file', file);

            fetch(response.uploadUrl, {
              method: 'PUT',
              body: file,
              headers: {
                'Content-Type': file.type
              }
            })
            .then(() => {
              observer.next({ url: response.fileUrl });
              observer.complete();
            })
            .catch(error => {
              observer.error(error);
            });
          },
          error: (error) => {
            observer.error(error);
          }
        });
    });
  }
}
```

### Step 25: Update Environment Configuration

**src/environments/environment.ts**
```typescript
export const environment = {
  production: false,
  apiUrl: 'http://localhost:3000/api' // For local development with SAM
};
```

**src/environments/environment.prod.ts**
```typescript
export const environment = {
  production: true,
  apiUrl: 'https://your-api-id.execute-api.us-east-1.amazonaws.com/prod'
};
```

### Step 26: Add Sample Data Migration Script

**scripts/migrate-data.js**
```javascript
const AWS = require('aws-sdk');
const fs = require('fs');
const path = require('path');

AWS.config.update({ region: 'us-east-1' });
const dynamodb = new AWS.DynamoDB.DocumentClient();

// Sample data from your existing readings
const sampleReadings = [
  {
    dateCode: '0918',
    date: 'September 18',
    dayOfWeek: 'Thursday',
    title: 'Ecclesiastes 7:13 - 10:7 & 1 Thessalonians 5',
    audioUrl: 'https://d24muyyuu3zj8g.cloudfront.net/2025/september/3/sept18.mp3',
    oldTestament: [
      {
        book: 'Ecclesiastes',
        chapter: '7:13-29',
        verses: [
          { number: 13, text: 'Consider the work of God: for who can make that straight, which he hath made crooked?' },
          { number: 14, text: 'In the day of prosperity be joyful, but in the day of adversity consider: God also hath set the one over against the other, to the end that man should find nothing after him.' }
          // Add more verses...
        ]
      }
    ],
    newTestament: [
      {
        book: '1 Thessalonians',
        chapter: '5',
        verses: [
          { number: 1, text: 'But of the times and the seasons, brethren, ye have no need that I write unto you.' }
          // Add more verses...
        ]
      }
    ]
  },
  {
    dateCode: '0922',
    date: 'September 22',
    dayOfWeek: 'Monday',
    title: 'Song of Solomon 6:11 - Isaiah 1:31',
    audioUrl: 'https://d24muyyuu3zj8g.cloudfront.net/2025/september/4/sept22.mp3',
    oldTestament: [
      {
        book: 'Song of Solomon',
        chapter: '6:11-13',
        verses: [
          { number: 11, text: 'I went down into the garden of nuts to see the fruits of the valley, and to see whether the vine flourished, and the pomegranates budded.' }
          // Add more verses...
        ]
      }
    ],
    newTestament: []
  }
];

async function migrateData() {
  console.log('Starting data migration...');
  
  for (const reading of sampleReadings) {
    try {
      reading.createdAt = new Date().toISOString();
      reading.updatedAt = new Date().toISOString();
      
      await dynamodb.put({
        TableName: 'BibleReadings',
        Item: reading
      }).promise();
      
      console.log(`✓ Migrated reading ${reading.dateCode}`);
    } catch (error) {
      console.error(`✗ Failed to migrate reading ${reading.dateCode}:`, error);
    }
  }
  
  console.log('Data migration completed!');
}

migrateData();
```

### Step 27: Local Development with SAM

**template.yaml** (for local testing)
```yaml
AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31

Globals:
  Function:
    Timeout: 30
    Runtime: nodejs18.x
    Environment:
      Variables:
        DYNAMODB_TABLE: BibleReadings

Resources:
  ReadingsCrudFunction:
    Type: AWS::Serverless::Function
    Properties:
      CodeUri: lambda/readings-crud/
      Handler: index.handler
      Events:
        GetReadings:
          Type: Api
          Properties:
            Path: /readings
            Method: get
        GetReading:
          Type: Api
          Properties:
            Path: /readings/{dateCode}
            Method: get
        CreateReading:
          Type: Api
          Properties:
            Path: /readings
            Method: post
        UpdateReading:
          Type: Api
          Properties:
            Path: /readings/{dateCode}
            Method: put
        DeleteReading:
          Type: Api
          Properties:
            Path: /readings/{dateCode}
            Method: delete
        GetAvailable:
          Type: Api
          Properties:
            Path: /readings/available
            Method: get

  AudioUploadFunction:
    Type: AWS::Serverless::Function
    Properties:
      CodeUri: lambda/audio-upload/
      Handler: index.handler
      Events:
        UploadAudio:
          Type: Api
          Properties:
            Path: /upload-audio
            Method: post
```

### Step 28: Build and Deploy

```bash
# Install SAM CLI for local development
pip install aws-sam-cli

# Test locally
sam build
sam local start-api

# Deploy to AWS
sam deploy --guided

# Build Angular for production
ng build --prod

# Deploy to S3 (create bucket first)
aws s3 sync dist/one-year-bible-admin s3://your-frontend-bucket --delete
```

### Step 29: Final Configuration

**Update CORS in API Gateway after deployment:**
```bash
# Enable CORS for all methods
aws apigateway put-method-response \
  --rest-api-id $API_ID \
  --resource-id $READINGS_ID \
  --http-method GET \
  --status-code 200 \
  --response-parameters method.response.header.Access-Control-Allow-Origin=false

aws apigateway put-integration-response \
  --rest-api-id $API_ID \
  --resource-id $READINGS_ID \
  --http-method GET \
  --status-code 200 \
  --response-parameters method.response.header.Access-Control-Allow-Origin="'*'"
```

This complete tutorial now includes:

✅ **Frontend**: Angular application with admin interface  
✅ **Backend**: AWS Lambda functions with DynamoDB  
✅ **Storage**: S3 for audio files  
✅ **API**: API Gateway with CORS support  
✅ **Data Migration**: Scripts to populate initial data  
✅ **Local Development**: SAM for testing  
✅ **Deployment**: Complete AWS deployment pipeline  

The application is now fully serverless and scalable on AWS!

---

Compact chat history?

---

You stopped your current work and asked me to work on the following task instead.

---

how does this work with previous and future years?

---

The current system uses date codes (MMDD format) which are year-agnostic, meaning the same readings repeat every year. Here's how to handle multiple years:

## Current System Limitations
- Date codes like "0922" (September 22) don't include year
- Same content repeats annually
- No year-specific customization

## Multi-Year Solutions

### Option 1: Year-Agnostic (Current Approach)
**Pros**: Simple, content reuses annually  
**Cons**: No year-specific content, no progress tracking

```typescript
// Current dateCode format
dateCode: "0922" // September 22 (any year)
```

### Option 2: Year-Specific Date Codes
**Update Models and Database**

```typescript
// New dateCode format includes year
dateCode: "20240922" // September 22, 2024
dateCode: "20250922" // September 22, 2025
```

**Update DynamoDB Structure**
```json
{
  "dateCode": "20240922",
  "year": 2024,
  "date": "September 22",
  "dayOfWeek": "Monday",
  "title": "Song of Solomon 6:11 - Isaiah 1:31"
}
```

**Update Angular Services**
```typescript
// src/app/services/reading.service.ts
getReading(year: number, month: number, day: number): Observable<Reading | null> {
  const yearStr = year.toString();
  const monthStr = (month + 1).toString().padStart(2, '0');
  const dayStr = day.toString().padStart(2, '0');
  const dateCode = `${yearStr}${monthStr}${dayStr}`;
  
  return this.http.get<Reading>(`${this.apiUrl}/readings/${dateCode}`);
}

getAvailableReadings(year: number): Observable<string[]> {
  return this.http.get<string[]>(`${this.apiUrl}/readings/available?year=${year}`);
}
```

**Update Calendar Component**
```typescript
// src/app/components/calendar-widget/calendar-widget.component.ts
@Input() currentYear: number = new Date().getFullYear();

onDateClick(day: any): void {
  if (day.inactive) return;
  
  const yearStr = this.currentYear.toString();
  const monthStr = (this.currentMonth + 1).toString().padStart(2, '0');
  const dayStr = day.day.toString().padStart(2, '0');
  const dateCode = `${yearStr}${monthStr}${dayStr}`;
  
  this.dateSelected.emit(dateCode);
}

// Add year navigation
previousYear(): void {
  this.currentYear--;
  this.loadAvailableReadings();
  this.generateCalendar();
}

nextYear(): void {
  this.currentYear++;
  this.loadAvailableReadings();
  this.generateCalendar();
}
```

**Update Lambda Function**
```javascript
// lambda/readings-crud/index.js
async function getAvailableReadings(event) {
  const year = event.queryStringParameters?.year;
  
  let filterExpression = undefined;
  let expressionAttributeValues = undefined;
  
  if (year) {
    filterExpression = 'begins_with(dateCode, :year)';
    expressionAttributeValues = { ':year': year };
  }
  
  const result = await dynamodb.scan({
    TableName: 'BibleReadings',
    ProjectionExpression: 'dateCode',
    FilterExpression: filterExpression,
    ExpressionAttributeValues: expressionAttributeValues
  }).promise();
  
  const dateCodes = result.Items.map(item => item.dateCode).sort();
  
  return {
    statusCode: 200,
    body: JSON.stringify(dateCodes)
  };
}
```

### Option 3: Hybrid Approach (Recommended)

**Use base readings with year-specific overrides**

```typescript
// Base reading (reusable)
interface BaseReading {
  dateCode: string; // "0922" 
  date: string;
  title: string;
  oldTestament: Scripture[];
  newTestament: Scripture[];
}

// Year-specific reading (overrides base)
interface YearReading extends BaseReading {
  dateCode: string; // "20240922"
  year: number;
  baseReadingCode?: string; // "0922" - references base reading
  audioUrl?: string; // Year-specific audio
  customContent?: any; // Year-specific additions
}
```

**Service Logic**
```typescript
getReading(year: number, month: number, day: number): Observable<Reading | null> {
  const monthStr = (month + 1).toString().padStart(2, '0');
  const dayStr = day.toString().padStart(2, '0');
  const yearDateCode = `${year}${monthStr}${dayStr}`;
  const baseDateCode = `${monthStr}${dayStr}`;
  
  // Try year-specific first, fallback to base reading
  return this.http.get<Reading>(`${this.apiUrl}/readings/${yearDateCode}`)
    .pipe(
      catchError(() => 
        this.http.get<Reading>(`${this.apiUrl}/readings/${baseDateCode}`)
      )
    );
}
```

**Lambda Function with Fallback**
```javascript
async function getReading(dateCode) {
  // Try exact match first
  let result = await dynamodb.get({
    TableName: 'BibleReadings',
    Key: { dateCode }
  }).promise();
  
  // If not found and it's a year-specific code, try base reading
  if (!result.Item && dateCode.length === 8) {
    const baseDateCode = dateCode.slice(4); // Extract MMDD
    result = await dynamodb.get({
      TableName: 'BibleReadings',
      Key: { dateCode: baseDateCode }
    }).promise();
  }
  
  return {
    statusCode: result.Item ? 200 : 404,
    body: JSON.stringify(result.Item || { error: 'Reading not found' })
  };
}
```

### Option 4: Reading Plans by Year

**Create different reading plans**
```typescript
interface ReadingPlan {
  id: string;
  name: string;
  year: number;
  description: string;
  readings: Reading[];
}

// Examples:
// - "kcm-2024": Kenneth Copeland 2024 plan
// - "kcm-2025": Kenneth Copeland 2025 plan  
// - "chronological-2024": Chronological Bible plan
```

## Recommended Implementation

**Use Option 3 (Hybrid)** for maximum flexibility:

1. **Base readings** (MMDD format) for standard content
2. **Year-specific overrides** (YYYYMMDD format) for custom content
3. **Fallback logic** in services
4. **Year navigation** in calendar widget
5. **Admin interface** supports both base and year-specific readings

This approach allows:
- ✅ Reusing content across years
- ✅ Year-specific customizations
- ✅ Backward compatibility
- ✅ Efficient storage
- ✅ Easy content management

The system automatically falls back to base readings when year-specific content isn't available, making it both flexible and efficient.

---

Compact chat history?

---

Compacting your chat history, this may take a moment.

---


## Conversation Summary
- **HTML/CSS Fixes**: Fixed CSS compatibility issues (user-select webkit prefix), broken Google Fonts URL, and missing meta elements (charset, viewport, title, lang attribute)
- **Calendar Navigation**: Implemented calendar widget with date navigation, Previous/Next day buttons, and "Today" button functionality
- **File Structure**: Organized readings into month-based folder structure (readings/september/) with consistent naming (MMDD.html format)
- **Scripture Pages**: Created individual reading pages (September 18-23) with complete scripture content, audio players, and calendar widgets
- **Angular Migration Planning**: Discussed converting the static HTML project to Angular with admin backend
- **AWS Serverless Architecture**: Designed complete serverless solution using Angular frontend, Lambda functions, DynamoDB, and S3 for audio files
- **Multi-Year Support**: Addressed how to handle readings across different years with hybrid approach using base readings and year-specific overrides

## Files and Code Summary
- **OneYearBible/style.css**: Added -webkit-user-select prefix for Safari compatibility
- **OneYearBible/index.html**: Fixed meta elements, added title and lang attributes, integrated calendar widget
- **OneYearBible/script.js**: Updated navigation logic to use month/day checking instead of day-of-year calculation, fixed September 22 navigation
- **OneYearBible/main-script.js**: Contains availableReadings array with date codes, calendar rendering logic, and navigation functions
- **OneYearBible/widget-script.js**: Calendar widget with dynamic date highlighting, Previous/Next navigation, and multi-page compatibility
- **OneYearBible/readings/september/**: Individual reading pages (0918.html, 0919.html, 0920.html, 0922.html) with complete scripture content
- **Lambda Functions**: readings-crud.js for CRUD operations, audio-upload.js for S3 file uploads with presigned URLs
- **Angular Components**: Calendar widget, reading pages, admin dashboard, and reading form components with reactive forms

## Key Insights
- **File Naming Convention**: Uses MMDD format (e.g., 0922.html for September 22) for consistent date-based navigation
- **Calendar Widget**: Reusable component that highlights current page date and available readings, works across all pages
- **Navigation Logic**: Uses month === 8 && day === 22 format instead of day-of-year calculations for more reliable date checking
- **AWS Architecture**: Serverless design with API Gateway → Lambda → DynamoDB for scalability and cost efficiency
- **Admin Interface**: Full CRUD operations with form validation, audio upload to S3, and reading management dashboard
- **Multi-Year Strategy**: Hybrid approach using base readings (MMDD) with year-specific overrides (YYYYMMDD) and fallback logic
- **Scripture Content**: Full verse-by-verse content with tabbed Old/New Testament sections and audio integration

## Most Recent Topic
**Topic**: Multi-year support for the Bible reading application
**Progress**: Discussed how the current MMDD date code system works across years and provided multiple approaches for handling year-specific content
**Tools Used**:
- **fsRead**: Read the 0926.html file to understand current file structure and date formatting
- **Analysis**: Examined how current year-agnostic system (MMDD format) handles recurring annual content and identified limitations for year-specific customization

The user asked about handling previous and future years in the application. The current system uses MMDD format (like "0922" for September 22) which is year-agnostic and repeats annually. Four solutions were presented: 1) Keep current year-agnostic approach, 2) Use year-specific codes (YYYYMMDD), 3) Hybrid approach with base readings and year overrides (recommended), and 4) Reading plans by year. The hybrid approach allows reusing content across years while enabling year-specific customizations through fallback logic in services.

---


Conversation history has been compacted successfully!