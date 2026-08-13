import { useEffect, useMemo, useRef, useState } from "react";
import { counties } from "@/data/countyData";
import { corridorSegments } from "@/data/corridorRoadData";
import { places } from "@/data/placeData";
import { roads } from "@/data/roadData";

/* Design reminder: minimalist cartography with actual OSM road geometry. The corridor overlay
   is composed of existing road segments only; it never draws waypoint-to-waypoint connectors. */

const bounds = { minLat: 43.15, maxLat: 45.15, minLng: -117.25, maxLng: -115.55 };
const viewBox = { width: 1120, height: 780 };
const MIN_SCALE = 1;
const MAX_SCALE = 5.5;
const overviewPlaces = new Set(["Boise", "Meridian", "Emmett", "Council", "Weiser", "Cambridge"]);

const corridorGroups = [
  { key: "id16", segments: corridorSegments.id16 ?? [], opacity: 0.96 },
  { key: "id52", segments: corridorSegments.id52 ?? [], opacity: 0.9 },
  { key: "sweetOla", segments: corridorSegments.sweetOla ?? [], opacity: 0.96 },
  { key: "existingRoadCandidates", segments: corridorSegments.existingRoadCandidates ?? [], opacity: 0.86 },
  { key: "adamsCandidate", segments: corridorSegments.adamsCandidate ?? [], opacity: 0.72 },
];

function project([lat, lng]: [number, number]) {
  const x = ((lng - bounds.minLng) / (bounds.maxLng - bounds.minLng)) * viewBox.width;
  const y = ((bounds.maxLat - lat) / (bounds.maxLat - bounds.minLat)) * viewBox.height;
  return [x, y] as const;
}

function pathFromPoints(points: [number, number][]) {
  return points.map((point, index) => {
    const [x, y] = project(point);
    return `${index === 0 ? "M" : "L"}${x.toFixed(1)} ${y.toFixed(1)}`;
  }).join(" ");
}

function roadStyle(highway: string) {
  if (highway === "motorway" || highway === "trunk") return { color: "#233840", width: 4.2, opacity: 0.94 };
  if (highway === "primary") return { color: "#49646c", width: 3.1, opacity: 0.9 };
  if (highway === "secondary") return { color: "#8b765f", width: 2.35, opacity: 0.84 };
  if (highway === "tertiary") return { color: "#789187", width: 1.75, opacity: 0.76 };
  return { color: "#9aaa9f", width: 1.0, opacity: 0.62 };
}

const countyLabels = counties.map((county) => {
  const allPoints = county.segments.flatMap((segment) => segment.points);
  if (!allPoints.length) return { name: county.name, position: [44, -116] as [number, number] };
  const lat = allPoints.reduce((sum, point) => sum + point[0], 0) / allPoints.length;
  const lng = allPoints.reduce((sum, point) => sum + point[1], 0) / allPoints.length;
  return { name: county.name, position: [lat, lng] as [number, number] };
});

export default function Home() {
  const svgRef = useRef<SVGSVGElement | null>(null);
  const dragRef = useRef({ active: false, x: 0, y: 0 });
  const [scale, setScale] = useState(1);
  const [offset, setOffset] = useState({ x: 0, y: 0 });
  const [showCorridor, setShowCorridor] = useState(true);

  const visibleRoads = useMemo(() => roads.filter((road) => {
    if (road.highway === "motorway" || road.highway === "trunk" || road.highway === "primary") return true;
    if (road.highway === "secondary") return scale >= 1.08;
    if (road.highway === "tertiary") return scale >= 1.65;
    return scale >= 2.5;
  }), [scale]);

  const visiblePlaces = useMemo(() => places.filter((place) => scale >= 1.6 || overviewPlaces.has(place.name)), [scale]);
  const countyTextOpacity = scale < 1.35 ? 0.82 : 0.55;
  const transform = `translate(${offset.x} ${offset.y}) scale(${scale})`;

  const zoomAt = (nextScale: number, anchor?: { x: number; y: number }) => {
    const svg = svgRef.current;
    if (!svg) return;
    const rect = svg.getBoundingClientRect();
    const anchorX = anchor?.x ?? rect.width / 2;
    const anchorY = anchor?.y ?? rect.height / 2;
    const svgX = (anchorX / rect.width) * viewBox.width;
    const svgY = (anchorY / rect.height) * viewBox.height;
    const clamped = Math.max(MIN_SCALE, Math.min(MAX_SCALE, nextScale));
    const ratio = clamped / scale;
    setOffset((current) => ({
      x: svgX - (svgX - current.x) * ratio,
      y: svgY - (svgY - current.y) * ratio,
    }));
    setScale(clamped);
  };

  const resetView = () => {
    setScale(1);
    setOffset({ x: 0, y: 0 });
  };

  useEffect(() => {
    const svg = svgRef.current;
    if (!svg) return;
    const handleWheel = (event: WheelEvent) => {
      event.preventDefault();
      const rect = svg.getBoundingClientRect();
      zoomAt(scale * (event.deltaY < 0 ? 1.22 : 0.82), { x: event.clientX - rect.left, y: event.clientY - rect.top });
    };
    svg.addEventListener("wheel", handleWheel, { passive: false });
    return () => svg.removeEventListener("wheel", handleWheel);
  }, [scale]);

  const handlePointerDown = (event: React.PointerEvent<SVGSVGElement>) => {
    dragRef.current = { active: true, x: event.clientX, y: event.clientY };
    svgRef.current?.setPointerCapture(event.pointerId);
  };

  const handlePointerMove = (event: React.PointerEvent<SVGSVGElement>) => {
    if (!dragRef.current.active || !svgRef.current) return;
    const rect = svgRef.current.getBoundingClientRect();
    const dx = ((event.clientX - dragRef.current.x) / rect.width) * viewBox.width;
    const dy = ((event.clientY - dragRef.current.y) / rect.height) * viewBox.height;
    dragRef.current = { active: true, x: event.clientX, y: event.clientY };
    setOffset((current) => ({ x: current.x + dx, y: current.y + dy }));
  };

  const endDrag = () => { dragRef.current.active = false; };

  return (
    <main className="h-screen w-screen overflow-hidden bg-[#dfe6de]">
      <svg ref={svgRef} viewBox={`0 0 ${viewBox.width} ${viewBox.height}`} preserveAspectRatio="xMidYMid slice" className="block h-full w-full touch-none select-none cursor-grab active:cursor-grabbing" role="img" aria-label="OpenStreetMap-based map of Ada, Gem, Adams, and Washington Counties" onPointerDown={handlePointerDown} onPointerMove={handlePointerMove} onPointerUp={endDrag} onPointerCancel={endDrag}>
        <defs>
          <linearGradient id="countyWash" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stopColor="#e7ece5" /><stop offset="56%" stopColor="#dbe5dc" /><stop offset="100%" stopColor="#eef0e8" /></linearGradient>
          <pattern id="topography" width="120" height="100" patternUnits="userSpaceOnUse" patternTransform="rotate(-10)"><path d="M-20 25 C10 3 38 4 66 25 S114 47 140 24" fill="none" stroke="#c3d0c5" strokeWidth="1.1" opacity="0.5" /><path d="M-20 67 C10 45 38 46 66 67 S114 89 140 66" fill="none" stroke="#c3d0c5" strokeWidth="1.1" opacity="0.4" /></pattern>
        </defs>
        <rect width={viewBox.width} height={viewBox.height} fill="url(#countyWash)" />
        <rect width={viewBox.width} height={viewBox.height} fill="url(#topography)" opacity="0.45" />

        <g transform={transform}>
          {counties.flatMap((county) => county.segments.map((segment, index) => <path key={`${county.name}-${index}`} d={pathFromPoints(segment.points)} fill="none" stroke="#87988d" strokeWidth={1.75 / scale} strokeDasharray={`${8 / scale} ${7 / scale}`} opacity="0.88" vectorEffect="non-scaling-stroke" />))}
          {visibleRoads.map((road, index) => { const style = roadStyle(road.highway); return <path key={`${road.name}-${index}`} d={pathFromPoints(road.points)} fill="none" stroke={style.color} strokeWidth={style.width / scale} strokeOpacity={style.opacity} strokeLinecap="round" strokeLinejoin="round" vectorEffect="non-scaling-stroke" />; })}

          {showCorridor && corridorGroups.flatMap((group) => group.segments.map((segment, index) => <g key={`${group.key}-${segment.name}-${index}`} opacity={group.opacity}><path d={pathFromPoints(segment.points)} fill="none" stroke="#fffaf1" strokeWidth={8 / scale} strokeLinecap="round" strokeLinejoin="round" vectorEffect="non-scaling-stroke" /><path d={pathFromPoints(segment.points)} fill="none" stroke="#c75a34" strokeWidth={4.2 / scale} strokeLinecap="round" strokeLinejoin="round" strokeDasharray={`${11 / scale} ${8 / scale}`} vectorEffect="non-scaling-stroke" /></g>))}

          {visiblePlaces.map((place) => { const [x, y] = project(place.position); const isLarge = overviewPlaces.has(place.name); return <g key={place.name}><circle cx={x} cy={y} r={(isLarge ? 5.6 : 3.5) / scale} fill={isLarge ? "#243238" : "#617b78"} stroke="#edf0e8" strokeWidth={1.7 / scale} vectorEffect="non-scaling-stroke" /><text x={x + 9 / scale} y={y + (place.name === "Boise" ? 22 : -9) / scale} fontSize={(isLarge ? 15 : 11) / scale} fontWeight={isLarge ? 650 : 500} fill="#2b3a3f" vectorEffect="non-scaling-stroke">{place.name}</text></g>; })}
          {countyLabels.map((county) => { const [x, y] = project(county.position); return <text key={county.name} x={x} y={y} textAnchor="middle" fontSize={12 / scale} letterSpacing={2.2 / scale} fill="#75847d" opacity={countyTextOpacity} vectorEffect="non-scaling-stroke">{county.name.toUpperCase()}</text>; })}
        </g>

        <g transform="translate(1054 742)" className="pointer-events-none"><path d="M0 28 L0 0 L-7 10 L0 0 L7 10" fill="none" stroke="#43535a" strokeWidth="2" /><text x="-7" y="46" fontSize="10" fill="#667674">N</text></g>
      </svg>

      <div className="fixed bottom-2 left-2 flex items-center gap-1 rounded-sm bg-[#f2f1eb]/85 p-1 shadow-sm backdrop-blur-sm" aria-label="Map controls">
        <button type="button" onClick={() => zoomAt(scale * 1.35)} className="h-7 w-7 text-base leading-none text-[#344348] transition hover:bg-white" aria-label="Zoom in">+</button>
        <button type="button" onClick={() => zoomAt(scale * 0.74)} className="h-7 w-7 text-base leading-none text-[#344348] transition hover:bg-white" aria-label="Zoom out">−</button>
        <button type="button" onClick={resetView} className="h-7 px-2 text-[10px] uppercase tracking-[0.12em] text-[#52625f] transition hover:bg-white" aria-label="Reset map view">Reset</button>
        <button type="button" onClick={() => setShowCorridor((current) => !current)} className={`h-7 px-2.5 text-[10px] font-semibold uppercase tracking-[0.1em] transition ${showCorridor ? "bg-[#c75a34] text-white" : "text-[#52625f] hover:bg-white"}`} aria-label="Toggle existing route improvement overlay">Existing routes</button>
      </div>
      <div className="pointer-events-none fixed bottom-1 right-2 bg-[#f2f1eb]/80 px-1.5 py-0.5 text-[10px] text-[#52625f]">© OpenStreetMap contributors</div>
    </main>
  );
}
