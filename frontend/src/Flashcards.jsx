import { useState } from 'react';
import { useSpring, animated } from '@react-spring/web';

function FlashCard({ card }) {
  const [flipped, setFlipped] = useState(false);
  const { transform, opacity } = useSpring({
    opacity: flipped ? 1 : 0,
    transform: `perspective(600px) rotateY(${flipped ? 180 : 0}deg)`,
    config: { mass: 5, tension: 500, friction: 80 },
  });

  return (
    <div
      className="relative h-40 cursor-pointer"
      onClick={() => setFlipped((s) => !s)}
    >
      <animated.div
        className="absolute inset-0 flex items-center justify-center rounded-lg bg-white/10 p-4 backface-hidden"
        style={{ opacity: opacity.to((o) => 1 - o), transform }}
      >
        <p className="text-center font-medium">{card.q}</p>
      </animated.div>
      <animated.div
        className="absolute inset-0 flex items-center justify-center rounded-lg bg-blue-900/30 p-4 backface-hidden"
        style={{
          opacity,
          transform: transform.to((t) => `${t} rotateY(180deg)`),
        }}
      >
        <p className="text-center text-gray-200">{card.a}</p>
      </animated.div>
    </div>
  );
}

export default function Flashcards({ cards }) {
  return (
    <section>
      <h2 className="mb-2 text-xl font-bold">Flashcards</h2>
      <div className="grid gap-3">
        {cards.map((card, i) => (
          <FlashCard key={i} card={card} />
        ))}
      </div>
    </section>
  );
}
