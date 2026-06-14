import { createFileRoute } from "@tanstack/react-router";
import { useEffect, useMemo, useState } from "react";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";

export const Route = createFileRoute("/")({
  head: () => ({
    meta: [
      { title: "Brawl Memory — Match the Brawlers" },
      {
        name: "description",
        content:
          "A memory card matching game featuring Brawl Stars brawlers. Flip, match, and beat your best time.",
      },
      { property: "og:title", content: "Brawl Memory — Match the Brawlers" },
      {
        property: "og:description",
        content:
          "A memory card matching game featuring Brawl Stars brawlers. Flip, match, and beat your best time.",
      },
    ],
  }),
  component: Index,
});

type Brawler = { id: number; name: string };

// Brawler portraits served by the public Brawlify CDN.
const BRAWLERS: Brawler[] = [
  { id: 16000000, name: "Shelly" },
  { id: 16000001, name: "Colt" },
  { id: 16000002, name: "Bull" },
  { id: 16000003, name: "Brock" },
  { id: 16000004, name: "Rico" },
  { id: 16000005, name: "Spike" },
  { id: 16000006, name: "Barley" },
  { id: 16000007, name: "Jessie" },
  { id: 16000008, name: "Nita" },
  { id: 16000009, name: "Dynamike" },
  { id: 16000010, name: "El Primo" },
  { id: 16000011, name: "Mortis" },
];

const portraitUrl = (id: number) =>
  `https://cdn.brawlify.com/brawlers/borderless/${id}.png`;

type Card = {
  key: string;
  brawler: Brawler;
  flipped: boolean;
  matched: boolean;
};

const DIFFICULTIES = {
  Easy: 6,
  Medium: 8,
  Hard: 12,
} as const;
type Difficulty = keyof typeof DIFFICULTIES;

function shuffle<T>(arr: T[]): T[] {
  const a = [...arr];
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

function buildDeck(pairs: number): Card[] {
  const picked = shuffle(BRAWLERS).slice(0, pairs);
  const doubled = picked.flatMap((b, i) => [
    { key: `${b.id}-a-${i}`, brawler: b, flipped: false, matched: false },
    { key: `${b.id}-b-${i}`, brawler: b, flipped: false, matched: false },
  ]);
  return shuffle(doubled);
}

function Index() {
  const [difficulty, setDifficulty] = useState<<Difficulty>("Medium");
  const [cards, setCards] = useState<<Card[]>([]);
  const [selected, setSelected] = useState<number[]>([]);
  const [moves, setMoves] = useState(0);
  const [seconds, setSeconds] = useState(0);
  const [started, setStarted] = useState(false);
  const [ready, setReady] = useState(false);

  useEffect(() => {
    setCards(buildDeck(DIFFICULTIES.Medium));
    setReady(true);
  }, []);

  const won = cards.length > 0 && cards.every((c) => c.matched);

  useEffect(() => {
    if (!started || won) return;
    const t = setInterval(() => setSeconds((s) => s + 1), 1000);
    return () => clearInterval(t);
  }, [started, won]);

  const reset = (d: Difficulty = difficulty) => {
    setDifficulty(d);
    setCards(buildDeck(DIFFICULTIES[d]));
    setSelected([]);
    setMoves(0);
    setSeconds(0);
    setStarted(false);
  };

  const handleFlip = (idx: number) => {
    if (!started) setStarted(true);
    const c = cards[idx];
    if (c.flipped || c.matched || selected.length === 2) return;

    const next = cards.map((card, i) =>
      i === idx ? { ...card, flipped: true } : card,
    );
    const nextSelected = [...selected, idx];
    setCards(next);
    setSelected(nextSelected);

    if (nextSelected.length === 2) {
      setMoves((m) => m + 1);
      const [a, b] = nextSelected;
      if (next[a].brawler.id === next[b].brawler.id) {
        setTimeout(() => {
          setCards((cs) =>
            cs.map((card, i) =>
              i === a || i === b ? { ...card, matched: true } : card,
            ),
          );
          setSelected([]);
        }, 400);
      } else {
        setTimeout(() => {
          setCards((cs) =>
            cs.map((card, i) =>
              i === a || i === b ? { ...card, flipped: false } : card,
            ),
          );
          setSelected([]);
        }, 850);
      }
    }
  };

  const gridCols = useMemo(() => {
    const n = cards.length;
    if (n <= 12) return "grid-cols-3 sm:grid-cols-4";
    if (n <= 16) return "grid-cols-4";
    return "grid-cols-4 sm:grid-cols-6";
  }, [cards.length]);

  const matchedPairs = cards.filter((c) => c.matched).length / 2;
  const totalPairs = cards.length / 2;

  return (
    <div className="min-h-screen bg-gradient-to-br from-background via-background to-muted">
      <div className="mx-auto max-w-4xl px-4 py-8">
        <header className="mb-6 text-center">
          <h1 className="bg-gradient-to-r from-primary to-accent-foreground bg-clip-text text-4xl font-extrabold tracking-tight text-transparent sm:text-5xl">
            Brawl Memory
          </h1>
          <p className="mt-2 text-muted-foreground">
            Match every brawler pair. Fewer moves = better score.
          </p>
        </header>

        <div className="mb-6 flex flex-wrap items-center justify-between gap-3 rounded-lg border bg-card p-4 shadow-sm">
          <div className="flex gap-2">
            {(Object.keys(DIFFICULTIES) as Difficulty[]).map((d) => (
              <Button
                key={d}
                size="sm"
                variant={d === difficulty ? "default" : "outline"}
                onClick={() => reset(d)}
              >
                {d}
              </Button>
            ))}
          </div>
          <div className="flex items-center gap-4 text-sm font-medium">
            <span> {seconds}s</span>
            <span> {moves} moves</span>
            <span>
               {matchedPairs}/{totalPairs}
            </span>
            <Button size="sm" variant="secondary" onClick={() => reset()}>
              Restart
            </Button>
          </div>
        </div>

        {won && (
          <div className="mb-6 rounded-lg border border-primary/40 bg-primary/10 p-4 text-center">
            <p className="text-lg font-bold"> You won in {moves} moves & {seconds}s!</p>
            <Button className="mt-3" onClick={() => reset()}>
              Play again
            </Button>
          </div>
        )}

        {!ready ? (
          <div className="flex h-64 items-center justify-center text-muted-foreground">
            Loading brawlers
          </div>
        ) : (
          <div className={cn("grid gap-3", gridCols)}>
            {cards.map((card, idx) => {
              const showFace = card.flipped || card.matched;
              return (
                <button
                  key={card.key}
                  onClick={() => handleFlip(idx)}
                  className="group [perspective:1000px] aspect-square"
                  aria-label={showFace ? card.brawler.name : "Hidden card"}
                >
                  <div
                    className={cn(
                      "relative h-full w-full transition-transform duration-500 [transform-style:preserve-3d]",
                      showFace && "[transform:rotateY(180deg)]",
                    )}
                  >
                    {/* Back */}
                    <div className="absolute inset-0 flex items-center justify-center rounded-xl border-2 border-primary/40 bg-gradient-to-br from-primary/80 to-primary shadow-md [backface-visibility:hidden] group-hover:scale-[1.02] transition-transform">
                      <span className="text-3xl font-black text-primary-foreground">?</span>
                    </div>
                    {/* Front */}
                    <div
                      className={cn(
                        "absolute inset-0 flex flex-col items-center justify-center gap-1 rounded-xl border-2 bg-card p-2 shadow-md [backface-visibility:hidden] [transform:rotateY(180deg)]",
                        card.matched ? "border-green-500" : "border-border",
                      )}
                    >
                      <img
                        src={portraitUrl(card.brawler.id)}
                        alt={card.brawler.name}
                        loading="lazy"
                        className="h-full w-full object-contain"
                      />
                      <span className="text-xs font-semibold">{card.brawler.name}</span>
                    </div>
                  </div>
                </button>
              );
            })}
          </div>
        )}

        <footer className="mt-8 text-center text-xs text-muted-foreground">
          Brawler artwork via the community Brawlify CDN. Not affiliated with Supercell.
        </footer>
      </div>
    </div>
  );
}
