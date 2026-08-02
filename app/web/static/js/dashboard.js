document.addEventListener(
    "DOMContentLoaded",
    function(){


        const canvas =
        document.getElementById(
            "transactionChart"
        );


        if(!canvas)
        {
            console.log(
                "Chart canvas tidak ditemukan"
            );

            return;
        }



        new Chart(
            canvas,
            {

            type:"bar",


            data:{


                labels:[

                    "Total",
                    "Pending",
                    "Success",
                    "Failed"

                ],



                datasets:[{


                    label:
                    "Transaksi",



                    data:[


                        window.totalTransaksi,


                        window.totalPending,


                        window.totalSuccess,


                        window.totalFailed


                    ]


                }]


            },


            options:{


                responsive:true,


                maintainAspectRatio:false


            }


            }

        );


    }
);