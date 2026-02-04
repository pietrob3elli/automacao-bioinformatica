# Bioinformatics Pipeline Dashboard

A Next.js dashboard for visualizing prokaryotic genome assembly results with a professional dark mode/lab aesthetic.

![Dashboard Screenshot](https://github.com/user-attachments/assets/d2adc3b9-dbbb-4ac4-ad93-fdf6fab53c80)

## Features

- **Summary Cards**: Display key metrics including Total Reads, Assembly Status, and Contig Count
- **Scatter Plot**: Interactive visualization correlating N50 and Number of Contigs using Recharts
- **Data Table**: Clean presentation of sample assembly metrics
- **Dark Mode Theme**: Professional scientific aesthetic with Tailwind CSS
- **Responsive Design**: Mobile-friendly layout

## Prerequisites

- Node.js 18+ 
- npm or yarn

## Installation

```bash
cd dashboard
npm install
```

## Development

Start the development server:

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser to see the result.

## Build

Create a production build:

```bash
npm run build
```

Start the production server:

```bash
npm start
```

## Data Source

The dashboard reads assembly statistics from `/data/sample_assembly_stats.csv` in the parent directory. The CSV should have the following format:

```csv
sample,contigs,total_length,n50,gc_content
sample1,45,4500000,125000,52.3
```

## Technology Stack

- **Framework**: Next.js 16 with TypeScript
- **Styling**: Tailwind CSS
- **Charts**: Recharts
- **Deployment**: Vercel-ready

## Project Structure

```
dashboard/
├── app/
│   ├── page.tsx          # Main dashboard page
│   ├── layout.tsx        # Root layout
│   └── globals.css       # Global styles
├── components/
│   ├── SummaryCard.tsx   # Summary metric cards
│   ├── N50ScatterPlot.tsx # Scatter plot visualization
│   └── DataTable.tsx     # Assembly metrics table
└── lib/
    └── data.ts           # Data loading utilities
```

## Customization

To modify the theme colors, edit `app/globals.css` and the component files in the `components/` directory. The color scheme uses Tailwind's slate palette for the dark mode aesthetic.

## Learn More

To learn more about Next.js, take a look at the following resources:

- [Next.js Documentation](https://nextjs.org/docs) - learn about Next.js features and API.
- [Learn Next.js](https://nextjs.org/learn) - an interactive Next.js tutorial.

## Deploy on Vercel

The easiest way to deploy your Next.js app is to use the [Vercel Platform](https://vercel.com/new?utm_medium=default-template&filter=next.js&utm_source=create-next-app&utm_campaign=create-next-app-readme) from the creators of Next.js.

Check out the [Next.js deployment documentation](https://nextjs.org/docs/app/building-your-application/deploying) for more details.
