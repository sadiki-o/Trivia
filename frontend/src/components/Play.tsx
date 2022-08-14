import { FC, useEffect, useState } from "react";
import { getCategories, getQuizzQuestions, verifyAnswer } from "../utils/fetchDataUtils";
import useStore from "../zustandStore/store";

const Play: FC = () => {
  const [
    categories,
    roundState,
    quizzQuestions,
    score,
    setCategories,
    setGameRound,
    setGameQuestions,
    setGameScore
  ] = useStore((state) => [
    state.categories,
    state.gameData.roundState,
    state.gameData.quizzQuestions,
    state.gameData.score,
    state.setCategories,
    state.setGameRound,
    state.setGameQuestions,
    state.setGameScore,
  ]);
  const [category, setCategory] = useState<number>(-1);
  const [currentQuestion, setCurrentQuestion] = useState<number>(0);
  const [currentAnswer, setCurrentAnswer] = useState<string>('')
  const [showScore, setShowScore] = useState<boolean>(false)

  const startGame = () => {
    getQuizzQuestions(category, quizzQuestions)
      .then((res) => {
        setGameQuestions(res)
        setGameRound("Start")
        setCurrentQuestion(0)
        setGameScore(0)
      })
      .catch((err) => {
        console.log(err)
      })
  }

  useEffect(() => {
    getCategories()
      .then((res) => {
        setCategories(res)
      })
      .catch((err) => {
        console.log(err)
      })
  }, []);

  return (
    <div className="w-[70%] mx-auto mt-3 md:w-[40%]">
      {roundState == 'End' && !showScore ? (
        <>
          <label className="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2 text-center">
            Category :{" "}
          </label>
          <select
            defaultValue={0}
            onChange={(e) => setCategory(parseInt(e.currentTarget.value))}
            className=" block w-full bg-gray-200 text-gray-700 border border-gray-200 rounded py-3 px-4 leading-tight focus:outline-none focus:bg-white focus:border-gray-500 required:"
          >
            <option value="-1">all categories</option>
            {categories.map((cat) => (
              <option key={cat.id} value={cat.id}>
                {cat.type}
              </option>
            ))}
          </select>
          <br />

          <button
            onClick={startGame}
            className="block w-20 h-20 rounded-full bg-red-500 hover:bg-red-400 text-white font-bold text-lg mx-auto"
          >
            Play
          </button>
        </>
      ) : roundState == 'Start' && !showScore ? (
        <>
          <p className="font-bold text-black underline my-10">Question {currentQuestion! + 1} :</p>
          <h3 className="text-gray-600 text-lg ">
            {quizzQuestions![currentQuestion!].question}
          </h3>

          <input className="inline-block w-[90%] md:w-[60%] h-12 text-gray-600 rounded p-1 mt-8 mr-2" type="text" placeholder="Enter your answer" value={currentAnswer} onChange={(e) => setCurrentAnswer(e.currentTarget.value)} />

          <button onClick={(e) => {
            verifyAnswer(quizzQuestions![currentQuestion!].id!, currentAnswer)
              .then(res => {
                res ? setGameScore(score + 1) : null
              })
            if (e.currentTarget.innerText === "Show results") {
              setShowScore(true)
              setGameRound('End')
              return
            }
            setCurrentQuestion(currentQuestion! + 1)
            setCurrentAnswer('')
          }} className="text-white disabled:bg-gray-500 bg-blue-700 text-lg p-2 rounded font-bold"
            disabled={currentAnswer ? false : true}
          >{currentQuestion! < 4 ? "Next Question" : "Show results"}</button>
        </>
      ) : (
        <div className="flex flex-col justify-around items-center p-4 border-2 border-black ">
          <p className="text-2xl font-bold my-8" > Answers Score :</p>
          <div className="font-bold text-xl flex gap-3 justify-between mb-4 flex-wrap">
            <div className="p-2 rounded border-black text-white bg-teal-700">
              Correct : {score}
            </div>
            <div className="p-2 rounded border-black text-white bg-red-500">
              Incorrect : {5 - score}
            </div>
          </div>
          <button onClick={() => {
            setShowScore(false)
            setCurrentAnswer('')
            setGameScore(0)
            setCurrentQuestion(0)
          }}
            className="bg-blue-700 text-white p-3 rounded text-lg font-bold"
          >play Again</button>
        </div>
      )}

    </div>
  );
};

export default Play;
